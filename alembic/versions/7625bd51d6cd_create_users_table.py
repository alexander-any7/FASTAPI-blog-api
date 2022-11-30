"""create users table

Revision ID: 7625bd51d6cd
Revises: cb54c713463d
Create Date: 2022-11-26 23:41:27.728727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7625bd51d6cd'
down_revision = 'cb54c713463d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
