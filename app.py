import os
import secrets
from pathlib import Path

import click
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from auth_service import (
    AuthError,
    alterar_senha_cliente,
    autenticar_cliente,
    cadastrar_ou_atualizar_cliente,
)
from checkout_service import (
    CheckoutError,
    EstoqueInsuficienteError,
    criar_pedido,
    validar_dados_checkout,
)
from extensions import db
from models import Categoria, Cliente, ItemPedido, Pedido, Produto


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env.local")
load_dotenv(BASE_DIR / ".env")


def normalizar_database_url(database_url):
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL não configurada. Execute 'neon link' ou crie um arquivo .env.local."
        )

    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
    SQLALCHEMY_DATABASE_URI=normalizar_database_url(os.getenv("DATABASE_URL")),
    SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True, "pool_recycle": 300},
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
    MAX_CONTENT_LENGTH=16 * 1024,
)
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)


def listar_produtos():
    comando = (
        select(Produto)
        .where(Produto.estoque > 0)
        .options(joinedload(Produto.categoria))
        .order_by(Produto.id)
    )
    produtos = db.session.scalars(comando).all()
    return [produto.para_catalogo() for produto in produtos]


def ler_carrinho():
    carrinho_salvo = session.get("carrinho", {})
    if not isinstance(carrinho_salvo, dict):
        return {}

    carrinho = {}
    for produto_id, quantidade in carrinho_salvo.items():
        try:
            produto_id_int = int(produto_id)
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            continue

        if produto_id_int > 0 and quantidade_int > 0:
            carrinho[str(produto_id_int)] = quantidade_int
    return carrinho


def salvar_carrinho(carrinho):
    session["carrinho"] = carrinho
    session.modified = True


def resposta_carrinho(carrinho):
    if not carrinho:
        return {"itens": [], "quantidade_total": 0}

    ids = [int(produto_id) for produto_id in carrinho]
    ids_existentes = set(
        db.session.scalars(select(Produto.id).where(Produto.id.in_(ids))).all()
    )
    carrinho_valido = {
        produto_id: quantidade
        for produto_id, quantidade in carrinho.items()
        if int(produto_id) in ids_existentes
    }

    if carrinho_valido != carrinho:
        salvar_carrinho(carrinho_valido)

    itens = [
        {"id": int(produto_id), "quantity": quantidade}
        for produto_id, quantidade in sorted(
            carrinho_valido.items(), key=lambda item: int(item[0])
        )
    ]
    return {
        "itens": itens,
        "quantidade_total": sum(item["quantity"] for item in itens),
    }


def erro_json(mensagem, status):
    return jsonify({"erro": mensagem}), status


def cliente_logado():
    cliente_id = session.get("cliente_id")
    if cliente_id is None:
        return None
    try:
        return db.session.get(Cliente, int(cliente_id))
    except (TypeError, ValueError):
        session.pop("cliente_id", None)
        return None


def exigir_login():
    cliente = cliente_logado()
    if cliente is None:
        return None, redirect(url_for("login", proximo=request.path))
    return cliente, None


@app.context_processor
def contexto_autenticacao():
    return {"cliente_logado": cliente_logado()}


@app.get("/")
def catalogo():
    produtos = listar_produtos()
    return render_template("index.html", produtos=produtos)


@app.get("/carrinho")
def carrinho():
    return render_template("carrinho.html", produtos=listar_produtos())


@app.get("/checkout")
def checkout():
    return render_template(
        "checkout.html", produtos=listar_produtos(), cliente=cliente_logado()
    )


@app.get("/sucesso")
def sucesso():
    return render_template("sucesso.html", produtos=[])


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        try:
            with db.session.begin():
                cliente = cadastrar_ou_atualizar_cliente(request.form, db.session)
            session["cliente_id"] = cliente.id
            return redirect(url_for("meus_pedidos"))
        except AuthError as exc:
            erro = str(exc)
        except SQLAlchemyError:
            db.session.rollback()
            app.logger.exception("Falha de banco ao cadastrar cliente")
            erro = "Não foi possível concluir o cadastro."

    return render_template("cadastro.html", produtos=[], erro=erro)


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    proximo = request.args.get("proximo") or url_for("meus_pedidos")

    if request.method == "POST":
        try:
            cliente = autenticar_cliente(
                request.form.get("email"), request.form.get("senha"), db.session
            )
            session["cliente_id"] = cliente.id
            destino = (
                proximo
                if proximo.startswith("/") and not proximo.startswith("//")
                else url_for("meus_pedidos")
            )
            return redirect(destino)
        except AuthError as exc:
            erro = str(exc)

    return render_template("login.html", produtos=[], erro=erro)


@app.post("/logout")
def logout():
    session.pop("cliente_id", None)
    return redirect(url_for("catalogo"))


@app.get("/meus-pedidos")
def meus_pedidos():
    cliente, resposta = exigir_login()
    if resposta is not None:
        return resposta

    pedidos = db.session.scalars(
        select(Pedido)
        .where(Pedido.cliente_id == cliente.id)
        .options(joinedload(Pedido.itens).joinedload(ItemPedido.produto))
        .order_by(Pedido.criado_em.desc())
    ).unique().all()
    return render_template(
        "meus_pedidos.html", produtos=[], cliente=cliente, pedidos=pedidos
    )


@app.route("/alterar-senha", methods=["GET", "POST"])
def alterar_senha():
    cliente, resposta = exigir_login()
    if resposta is not None:
        return resposta

    erro = None
    sucesso_senha = False
    if request.method == "POST":
        try:
            alterar_senha_cliente(
                cliente,
                request.form.get("senha_atual"),
                request.form.get("nova_senha"),
                request.form.get("confirmar_senha"),
            )
            db.session.commit()
            sucesso_senha = True
        except AuthError as exc:
            db.session.rollback()
            erro = str(exc)
        except SQLAlchemyError:
            db.session.rollback()
            app.logger.exception("Falha de banco ao alterar senha")
            erro = "Não foi possível alterar a senha."

    return render_template(
        "alterar_senha.html",
        produtos=[],
        cliente=cliente,
        erro=erro,
        sucesso_senha=sucesso_senha,
    )


@app.get("/api/carrinho")
def consultar_carrinho():
    return jsonify(resposta_carrinho(ler_carrinho()))


@app.post("/api/carrinho/itens/<int:produto_id>")
def adicionar_item(produto_id):
    dados = request.get_json(silent=True) or {}
    quantidade = dados.get("quantidade", 1)
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        return erro_json("A quantidade deve ser um número inteiro positivo.", 400)

    produto = db.session.get(Produto, produto_id)
    if produto is None:
        return erro_json("Produto não encontrado.", 404)

    carrinho_atual = ler_carrinho()
    nova_quantidade = carrinho_atual.get(str(produto_id), 0) + quantidade
    if nova_quantidade > produto.estoque:
        return erro_json("A quantidade solicitada supera o estoque disponível.", 409)

    carrinho_atual[str(produto_id)] = nova_quantidade
    salvar_carrinho(carrinho_atual)
    return jsonify(resposta_carrinho(carrinho_atual)), 201


@app.patch("/api/carrinho/itens/<int:produto_id>")
def alterar_item(produto_id):
    dados = request.get_json(silent=True) or {}
    alteracao = dados.get("alteracao")
    if isinstance(alteracao, bool) or not isinstance(alteracao, int) or alteracao not in (-1, 1):
        return erro_json("A alteração de quantidade deve ser -1 ou 1.", 400)

    carrinho_atual = ler_carrinho()
    chave = str(produto_id)
    if chave not in carrinho_atual:
        return erro_json("O produto não está no carrinho.", 404)

    nova_quantidade = carrinho_atual[chave] + alteracao
    if nova_quantidade <= 0:
        carrinho_atual.pop(chave)
    else:
        produto = db.session.get(Produto, produto_id)
        if produto is None:
            carrinho_atual.pop(chave)
            salvar_carrinho(carrinho_atual)
            return erro_json("Produto não encontrado.", 404)
        if nova_quantidade > produto.estoque:
            return erro_json("A quantidade solicitada supera o estoque disponível.", 409)
        carrinho_atual[chave] = nova_quantidade

    salvar_carrinho(carrinho_atual)
    return jsonify(resposta_carrinho(carrinho_atual))


@app.delete("/api/carrinho/itens/<int:produto_id>")
def remover_item(produto_id):
    carrinho_atual = ler_carrinho()
    carrinho_atual.pop(str(produto_id), None)
    salvar_carrinho(carrinho_atual)
    return jsonify(resposta_carrinho(carrinho_atual))


@app.post("/api/checkout")
def finalizar_checkout():
    carrinho_atual = ler_carrinho()
    if not carrinho_atual:
        return erro_json("O carrinho está vazio.", 400)

    try:
        dados_checkout = validar_dados_checkout(request.get_json(silent=True))
        with db.session.begin():
            cliente = cliente_logado()
            pedido_id = criar_pedido(
                carrinho_atual,
                dados_checkout,
                cliente_id=cliente.id if cliente else None,
            )
    except EstoqueInsuficienteError as erro:
        return erro_json(str(erro), 409)
    except CheckoutError as erro:
        return erro_json(str(erro), 400)
    except SQLAlchemyError:
        db.session.rollback()
        app.logger.exception("Falha de banco ao finalizar o pedido")
        return erro_json("Não foi possível concluir o pedido. Tente novamente.", 503)

    session.pop("carrinho", None)
    return jsonify({"pedido_id": pedido_id}), 201


@app.cli.command("check-db")
def check_db():
    """Confere a conexão e as tabelas sem alterar o banco."""
    db.session.execute(text("SELECT 1"))
    contagens = {
        "categorias": db.session.scalar(select(func.count()).select_from(Categoria)),
        "clientes": db.session.scalar(select(func.count()).select_from(Cliente)),
        "produtos": db.session.scalar(select(func.count()).select_from(Produto)),
        "pedidos": db.session.scalar(select(func.count()).select_from(Pedido)),
        "itens_pedido": db.session.scalar(select(func.count()).select_from(ItemPedido)),
    }
    click.echo("Conexão com o Neon confirmada.")
    for tabela, quantidade in contagens.items():
        click.echo(f"- {tabela}: {quantidade} registro(s)")


@app.errorhandler(SQLAlchemyError)
def tratar_erro_de_banco(erro):
    db.session.rollback()
    app.logger.exception("Falha ao acessar o banco de dados", exc_info=erro)
    if request.path.startswith("/api/"):
        return erro_json("Banco de dados temporariamente indisponível.", 503)
    return "Não foi possível acessar o catálogo neste momento.", 503


if __name__ == "__main__":
    app.run(debug=True)
