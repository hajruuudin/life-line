"""add family member extended fields

Revision ID: c3d4e5f6g7h8
Revises: b2c3d4e5f6g7
Create Date: 2026-01-15 21:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6g7h8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6g7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add gender, profession, and health_notes columns to family_members."""
    op.add_column('family_members', sa.Column('gender', sa.String(20), nullable=True))
    op.add_column('family_members', sa.Column('profession', sa.String(255), nullable=True))
    op.add_column('family_members', sa.Column('health_notes', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove gender, profession, and health_notes columns from family_members."""
    op.drop_column('family_members', 'health_notes')
    op.drop_column('family_members', 'profession')
    op.drop_column('family_members', 'gender')
