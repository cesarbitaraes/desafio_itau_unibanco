"""create_table_taxas

Revision ID: 213cfac10167
Revises: 
Create Date: 2022-02-08 21:14:40.340205

"""
from alembic import op
import sqlalchemy as sa

from src.models.clients import ClientOptions
from src.models.clients import TaxType


# revision identifiers, used by Alembic.
revision = '213cfac10167'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'taxa',
        sa.Column('tax_pk_taxa', sa.Integer, primary_key=True),
        sa.Column('tax_en_cliente', sa.Enum(ClientOptions), nullable=False),
        sa.Column('tax_en_tipo', sa.Enum(TaxType), nullable=False),
        sa.Column('tax_vl_valor', sa.Float, nullable=False),
        sa.Column('tax_dt_criacao', sa.DateTime, server_default=sa.text('now()'), nullable=False),
        sa.Column('tax_dt_atualizacao', sa.DateTime, nullable=True)
    )


def downgrade():
    op.drop_table('taxa')
    op.execute('DROP TYPE ClientOptions')
    op.execute('DROP TYPE TaxType')
