"""schema inicial do TechStore

Revision ID: 20260902_01
Revises: 
Create Date: 2026-09-02 20:35:48.541061

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '20260902_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    existing_tables = set(inspect(bind).get_table_names())
    expected_tables = {
        "categorias",
        "clientes",
        "produtos",
        "pedidos",
        "itens_pedido",
    }

    # The schema may have been created before Alembic was introduced.
    # Let Alembic stamp this revision without destroying existing data.
    if expected_tables.issubset(existing_tables):
        return

    if existing_tables.intersection(expected_tables):
        missing_tables = sorted(expected_tables - existing_tables)
        raise RuntimeError(
            "Schema parcialmente criado; tabelas ausentes: "
            + ", ".join(missing_tables)
        )

    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=160), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "produtos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=140), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("preco", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "estoque",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "estoque >= 0", name="ck_produtos_estoque_nao_negativo"
        ),
        sa.CheckConstraint("preco >= 0", name="ck_produtos_preco_nao_negativo"),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_produtos_nome", "produtos", ["nome"], unique=False)
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'CRIADO'"),
            nullable=False,
        ),
        sa.Column(
            "total",
            sa.Numeric(precision=10, scale=2),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("cep", sa.String(length=12), nullable=False),
        sa.Column("cidade", sa.String(length=100), nullable=False),
        sa.Column("estado", sa.CHAR(length=2), nullable=False),
        sa.Column("endereco", sa.String(length=180), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("total >= 0", name="ck_pedidos_total_nao_negativo"),
        sa.ForeignKeyConstraint(["cliente_id"], ["clientes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_pedidos_cliente", "pedidos", ["cliente_id"], unique=False
    )
    op.create_table(
        "itens_pedido",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("produto_id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column(
            "preco_unitario", sa.Numeric(precision=10, scale=2), nullable=False
        ),
        sa.CheckConstraint(
            "preco_unitario >= 0", name="ck_itens_preco_nao_negativo"
        ),
        sa.CheckConstraint(
            "quantidade > 0", name="ck_itens_quantidade_positiva"
        ),
        sa.ForeignKeyConstraint(
            ["pedido_id"], ["pedidos.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["produto_id"], ["produtos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_itens_pedido", "itens_pedido", ["pedido_id"], unique=False
    )


def downgrade():
    op.drop_index("idx_itens_pedido", table_name="itens_pedido")
    op.drop_table("itens_pedido")
    op.drop_index("idx_pedidos_cliente", table_name="pedidos")
    op.drop_table("pedidos")
    op.drop_index("idx_produtos_nome", table_name="produtos")
    op.drop_table("produtos")
    op.drop_table("clientes")
    op.drop_table("categorias")
