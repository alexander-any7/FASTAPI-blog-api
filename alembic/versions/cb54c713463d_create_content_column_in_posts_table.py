"""create content column in posts table

Revision ID: cb54c713463d
Revises: d1b5e4ad688f
Create Date: 2022-11-26 23:29:06.900008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb54c713463d'
down_revision = 'd1b5e4ad688f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
