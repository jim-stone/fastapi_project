"""create dict tables

Revision ID: 6b725b3cbbba
Revises: 
Create Date: 2023-05-30 15:24:13.858395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b725b3cbbba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('dictionary',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('dictionary')
