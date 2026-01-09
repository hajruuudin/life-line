"""create illness_logs table

Revision ID: a1b2c3d4e5f6
Revises: 77c08d9cfbad
Create Date: 2026-01-09 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '77c08d9cfbad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create illness_logs table."""
    op.execute("""
    CREATE TABLE illness_logs (
        id              SERIAL PRIMARY KEY,
        family_member_id INTEGER NOT NULL
            REFERENCES family_members
                ON DELETE CASCADE,
        illness_name    VARCHAR(255) NOT NULL,
        start_date      DATE NOT NULL,
        end_date        DATE,
        notes           TEXT,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX idx_illness_logs_family_member_id
        ON illness_logs (family_member_id);

    CREATE INDEX idx_illness_logs_start_date
        ON illness_logs (start_date);
    """)


def downgrade() -> None:
    """Drop illness_logs table."""
    op.execute("""
    DROP TABLE IF EXISTS illness_logs;
    """)
