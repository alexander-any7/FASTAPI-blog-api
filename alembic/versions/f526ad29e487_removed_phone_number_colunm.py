"""removed phone number colunm

Revision ID: f526ad29e487
Revises: 4bf6b09b2799
Create Date: 2022-11-28 18:59:00.197130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f526ad29e487'
down_revision = '4bf6b09b2799'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    pass
