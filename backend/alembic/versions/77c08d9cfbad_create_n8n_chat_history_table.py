"""create n8n chat history table

Revision ID: 77c08d9cfbad
Revises: 2236f2a63b38
Create Date: 2026-01-04 16:24:04.283402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '77c08d9cfbad'
down_revision: Union[str, Sequence[str], None] = '2236f2a63b38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "n8n_chat_histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("message", JSONB, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("n8n_chat_histories")
