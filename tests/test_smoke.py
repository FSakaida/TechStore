import unittest
import uuid
from unittest.mock import patch

from sqlalchemy import func, inspect, select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app import app
from checkout_service import DadosCheckout, criar_pedido
from extensions import db
from models import Categoria, Cliente, ItemPedido, Pedido, Produto


class TechStoreSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.contexto = app.app_context()
        cls.contexto.push()
        cls.produto = db.session.scalar(
            select(Produto)
            .where(Produto.estoque >= 2)
            .order_by(Produto.id)
            .limit(1)
        )
        if cls.produto is None:
            raise RuntimeError("O teste requer um produto com pelo menos 2 unidades.")
        cls.produto_id = cls.produto.id
        cls.estoque_inicial = cls.produto.estoque
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.contexto.pop()

    def test_paginas_e_catalogo(self):
        with app.test_client() as cliente_http:
            for caminho in ("/", "/carrinho", "/checkout", "/sucesso"):
                resposta = cliente_http.get(caminho)
                self.assertEqual(resposta.status_code, 200, caminho)

            catalogo = cliente_http.get("/").get_data(as_text=True)
            self.assertIn("products-data", catalogo)
            self.assertIn('"stock"', catalogo)

    def test_carrinho_em_sessao(self):
        with app.test_client() as cliente_http:
            resposta = cliente_http.post(
                f"/api/carrinho/itens/{self.produto_id}",
                json={"quantidade": 1},
            )
            self.assertEqual(resposta.status_code, 201)
            self.assertEqual(resposta.get_json()["quantidade_total"], 1)

            resposta = cliente_http.patch(
                f"/api/carrinho/itens/{self.produto_id}",
                json={"alteracao": 1},
            )
            self.assertEqual(resposta.status_code, 200)
            self.assertEqual(resposta.get_json()["quantidade_total"], 2)

            resposta = cliente_http.post(
                f"/api/carrinho/itens/{self.produto_id}",
                json={"quantidade": self.estoque_inicial + 1},
            )
            self.assertEqual(resposta.status_code, 409)

            resposta = cliente_http.delete(
                f"/api/carrinho/itens/{self.produto_id}"
            )
            self.assertEqual(resposta.status_code, 200)
            self.assertEqual(resposta.get_json()["quantidade_total"], 0)

    def test_checkout_invalido_nao_grava(self):
        with app.test_client() as cliente_http:
            cliente_http.post(
                f"/api/carrinho/itens/{self.produto_id}",
                json={"quantidade": 1},
            )
            resposta = cliente_http.post("/api/checkout", json={})
            self.assertEqual(resposta.status_code, 400)

    def test_rota_checkout_confirma_e_limpa_carrinho(self):
        dados = {
            "nome": "Teste de Rota",
            "email": "rota@example.com",
            "telefone": "(11) 99999-9999",
            "cep": "13000-000",
            "cidade": "Campinas",
            "estado": "SP",
            "endereco": "Rua de Teste",
            "numero": "100",
        }
        with app.test_client() as cliente_http:
            cliente_http.post(
                f"/api/carrinho/itens/{self.produto_id}",
                json={"quantidade": 1},
            )
            db.session.remove()
            with patch("app.criar_pedido", return_value=123):
                resposta = cliente_http.post("/api/checkout", json=dados)

            self.assertEqual(resposta.status_code, 201)
            self.assertEqual(resposta.get_json()["pedido_id"], 123)
            carrinho = cliente_http.get("/api/carrinho").get_json()
            self.assertEqual(carrinho["quantidade_total"], 0)

    def test_modelos_correspondem_ao_schema_neon(self):
        inspetor = inspect(db.engine)
        modelos = (Categoria, Cliente, Produto, Pedido, ItemPedido)

        for modelo in modelos:
            colunas_banco = {
                coluna["name"]
                for coluna in inspetor.get_columns(modelo.__tablename__)
            }
            colunas_modelo = set(modelo.__table__.columns.keys())
            self.assertEqual(colunas_banco, colunas_modelo, modelo.__tablename__)

    def test_checkout_com_rollback_controlado(self):
        email_teste = f"bloco4-{uuid.uuid4().hex}@example.com"
        dados = DadosCheckout(
            nome="Teste Bloco 4",
            email=email_teste,
            telefone="(11) 99999-9999",
            cep="13000-000",
            cidade="Campinas",
            estado="SP",
            endereco="Rua de Teste",
            numero="100",
        )

        conexao = db.engine.connect()
        transacao = conexao.begin()
        sessao_teste = Session(
            bind=conexao,
            join_transaction_mode="create_savepoint",
        )
        try:
            pedido_id = criar_pedido(
                {str(self.produto_id): 1},
                dados,
                sessao=sessao_teste,
            )
            pedido = sessao_teste.get(Pedido, pedido_id)
            quantidade_itens = sessao_teste.scalar(
                select(func.count())
                .select_from(ItemPedido)
                .where(ItemPedido.pedido_id == pedido_id)
            )
            produto = sessao_teste.get(Produto, self.produto_id)

            self.assertEqual(quantidade_itens, 1)
            self.assertEqual(produto.estoque, self.estoque_inicial - 1)
            self.assertGreater(pedido.total, 0)
        finally:
            sessao_teste.close()
            transacao.rollback()
            conexao.close()

        db.session.remove()
        cliente_persistido = db.session.scalar(
            select(Cliente).where(Cliente.email == email_teste)
        )
        produto_restaurado = db.session.get(Produto, self.produto_id)
        self.assertIsNone(cliente_persistido)
        self.assertEqual(produto_restaurado.estoque, self.estoque_inicial)

    def test_cadastro_cria_cliente_e_abre_historico(self):
        email_teste = f"cadastro-{uuid.uuid4().hex}@example.com"

        conexao = db.engine.connect()
        transacao = conexao.begin()
        sessao_teste = Session(
            bind=conexao,
            join_transaction_mode="create_savepoint",
        )
        try:
            with patch("app.db.session", sessao_teste):
                with app.test_client() as cliente_http:
                    resposta = cliente_http.post(
                        "/cadastro",
                        data={
                            "nome": "Cliente Cadastro",
                            "email": email_teste,
                            "telefone": "(11) 97777-6666",
                            "senha": "senha123",
                            "confirmar_senha": "senha123",
                        },
                        follow_redirects=True,
                    )
                    self.assertEqual(resposta.status_code, 200)
                    self.assertIn("Meus pedidos", resposta.get_data(as_text=True))
                    self.assertIsNotNone(
                        sessao_teste.scalar(
                            select(Cliente).where(Cliente.email == email_teste)
                        )
                    )
        finally:
            sessao_teste.close()
            transacao.rollback()
            conexao.close()

    def test_login_cadastro_historico_e_alteracao_de_senha(self):
        email_teste = f"login-{uuid.uuid4().hex}@example.com"

        conexao = db.engine.connect()
        transacao = conexao.begin()
        sessao_teste = Session(
            bind=conexao,
            join_transaction_mode="create_savepoint",
        )
        try:
            cliente = Cliente(
                nome="Cliente Login",
                email=email_teste,
                telefone="(11) 98888-7777",
                senha_hash=generate_password_hash("senha123"),
            )
            sessao_teste.add(cliente)
            sessao_teste.flush()
            pedido_id = criar_pedido(
                {str(self.produto_id): 1},
                DadosCheckout(
                    nome=cliente.nome,
                    email=cliente.email,
                    telefone=cliente.telefone,
                    cep="13000-000",
                    cidade="Campinas",
                    estado="SP",
                    endereco="Rua de Teste",
                    numero="100",
                ),
                sessao=sessao_teste,
                cliente_id=cliente.id,
            )
            sessao_teste.commit()

            with patch("app.db.session", sessao_teste):
                with app.test_client() as cliente_http:
                    resposta = cliente_http.get("/meus-pedidos")
                    self.assertEqual(resposta.status_code, 302)
                    self.assertIn("/login", resposta.headers["Location"])

                    resposta = cliente_http.post(
                        "/login",
                        data={"email": email_teste, "senha": "errada"},
                        follow_redirects=True,
                    )
                    self.assertEqual(resposta.status_code, 200)
                    self.assertIn(
                        "E-mail ou senha inválidos.",
                        resposta.get_data(as_text=True),
                    )

                    resposta = cliente_http.post(
                        "/login",
                        data={"email": email_teste, "senha": "senha123"},
                        follow_redirects=True,
                    )
                    self.assertEqual(resposta.status_code, 200)
                    pagina = resposta.get_data(as_text=True)
                    self.assertIn("Meus pedidos", pagina)
                    self.assertIn(f"Pedido #{pedido_id}", pagina)

                    resposta = cliente_http.post(
                        "/alterar-senha",
                        data={
                            "senha_atual": "senha123",
                            "nova_senha": "nova456",
                            "confirmar_senha": "nova456",
                        },
                        follow_redirects=True,
                    )
                    self.assertEqual(resposta.status_code, 200)
                    self.assertIn(
                        "Senha alterada com sucesso.",
                        resposta.get_data(as_text=True),
                    )

                    cliente_http.post("/logout", follow_redirects=True)
                    resposta = cliente_http.post(
                        "/login",
                        data={"email": email_teste, "senha": "nova456"},
                        follow_redirects=True,
                    )
                    self.assertEqual(resposta.status_code, 200)
                    self.assertIn(
                        f"Pedido #{pedido_id}",
                        resposta.get_data(as_text=True),
                    )
        finally:
            sessao_teste.close()
            transacao.rollback()
            conexao.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
