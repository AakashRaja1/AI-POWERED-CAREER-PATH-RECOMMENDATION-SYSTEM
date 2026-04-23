"""Add timestamp columns to User table

Revision ID: add_timestamps
Revises: 0c92a429e803
Create Date: 2025-04-16 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_timestamps'
down_revision: Union[str, Sequence[str], None] = '0c92a429e803'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add created_at and last_login columns to user table."""
    # Add created_at column with default value
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    # Add last_login column as nullable
    op.add_column('user', sa.Column('last_login', sa.DateTime(), nullable=True))
    # Add is_admin column if not exists
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    """Downgrade schema - Remove timestamp columns from user table."""
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'last_login')
    op.drop_column('user', 'created_at')
