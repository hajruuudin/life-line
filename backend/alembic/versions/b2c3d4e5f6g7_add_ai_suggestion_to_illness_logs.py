"""add ai_suggestion to illness_logs

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-15 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add ai_suggestion column to illness_logs table."""
    op.add_column('illness_logs', sa.Column('ai_suggestion', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove ai_suggestion column from illness_logs table."""
    op.drop_column('illness_logs', 'ai_suggestion')
