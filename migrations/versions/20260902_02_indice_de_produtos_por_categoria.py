"""indice de produtos por categoria

Revision ID: 20260902_02
Revises: 20260902_01
Create Date: 2026-09-02 20:37:57.420484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260902_02'
down_revision = '20260902_01'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "idx_produtos_categoria",
        "produtos",
        ["categoria_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("idx_produtos_categoria", table_name="produtos")
