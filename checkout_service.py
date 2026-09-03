import re
import secrets
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import func, select
from werkzeug.security import generate_password_hash

from extensions import db
from models import Cliente, ItemPedido, Pedido, Produto


class CheckoutError(ValueError):
    pass


class EstoqueInsuficienteError(CheckoutError):
    pass


@dataclass(frozen=True)
class DadosCheckout:
    nome: str
    email: str
    telefone: str
    cep: str
    cidade: str
    estado: str
    endereco: str
    numero: str


LIMITES = {
    "nome": 120,
    "email": 160,
    "telefone": 20,
    "cep": 12,
    "cidade": 100,
    "estado": 2,
    "endereco": 180,
    "numero": 20,
}


def _texto_obrigatorio(dados, campo):
    valor = dados.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise CheckoutError(f"Preencha o campo {campo}.")

    valor = " ".join(valor.split())
    if len(valor) > LIMITES[campo]:
        raise CheckoutError(
            f"O campo {campo} deve ter no máximo {LIMITES[campo]} caracteres."
        )
    return valor


def validar_dados_checkout(dados):
    if not isinstance(dados, dict):
        raise CheckoutError("Dados do checkout inválidos.")

    valores = {campo: _texto_obrigatorio(dados, campo) for campo in LIMITES}
    valores["email"] = valores["email"].lower()
    valores["estado"] = valores["estado"].upper()

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valores["email"]):
        raise CheckoutError("Informe um e-mail válido.")
    if not re.fullmatch(r"[A-Z]{2}", valores["estado"]):
        raise CheckoutError("Informe o estado com duas letras.")

    return DadosCheckout(**valores)


def criar_pedido(carrinho, dados, sessao=None, cliente_id=None):
    sessao = sessao if sessao is not None else db.session
    produtos_ids = sorted(int(produto_id) for produto_id in carrinho)
    comando = (
        select(Produto)
        .where(Produto.id.in_(produtos_ids))
        .order_by(Produto.id)
        .with_for_update()
    )
    produtos = sessao.scalars(comando).all()
    produtos_por_id = {produto.id: produto for produto in produtos}

    if len(produtos_por_id) != len(produtos_ids):
        raise CheckoutError("Um dos produtos do carrinho não existe mais.")

    cliente = sessao.get(Cliente, cliente_id) if cliente_id is not None else None
    if cliente_id is not None and cliente is None:
        raise CheckoutError("Cliente autenticado não encontrado.")

    if cliente is None:
        cliente = sessao.scalar(
            select(Cliente).where(func.lower(Cliente.email) == dados.email)
        )
    if cliente is None:
        cliente = Cliente(
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            senha_hash=generate_password_hash(secrets.token_urlsafe(32)),
        )
        sessao.add(cliente)
    else:
        cliente.nome = dados.nome
        cliente.telefone = dados.telefone

    pedido = Pedido(
        cliente=cliente,
        status="CRIADO",
        total=Decimal("0.00"),
        cep=dados.cep,
        cidade=dados.cidade,
        estado=dados.estado,
        endereco=dados.endereco,
        numero=dados.numero,
    )
    sessao.add(pedido)

    total = Decimal("0.00")
    for produto_id in produtos_ids:
        produto = produtos_por_id[produto_id]
        quantidade = carrinho[str(produto_id)]

        if quantidade > produto.estoque:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}."
            )

        produto.estoque -= quantidade
        total += produto.preco * quantidade
        pedido.itens.append(
            ItemPedido(
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco,
            )
        )

    pedido.total = total
    sessao.flush()
    return pedido.id
