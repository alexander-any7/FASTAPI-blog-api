"""add foreign key to posts table

Revision ID: ad2253a38e29
Revises: 7625bd51d6cd
Create Date: 2022-11-26 23:59:54.026581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad2253a38e29'
down_revision = '7625bd51d6cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=False),)
    op.create_foreign_key('posts_users_fk',source_table='posts' ,referent_table='users',
        local_cols=['author_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'author_id')
    pass
