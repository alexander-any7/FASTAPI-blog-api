"""add colums to post table

Revision ID: 2ea2249c1838
Revises: ad2253a38e29
Create Date: 2022-11-28 15:04:14.011100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ea2249c1838'
down_revision = 'ad2253a38e29'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                        server_default=sa.text('NOW()'), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
