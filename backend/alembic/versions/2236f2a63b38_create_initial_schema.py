"""create initial schema

Revision ID: 2236f2a63b38
Revises: 
Create Date: 2026-01-04 12:03:39.375057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2236f2a63b38'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    create table users
    (
        id                   serial
            primary key,
        email                varchar(255) not null
            unique,
        name                 varchar(255),
        google_id            varchar(255)
            unique,
        google_oauth_token   text,
        google_refresh_token text,
        created_at           timestamp default CURRENT_TIMESTAMP,
        updated_at           timestamp default CURRENT_TIMESTAMP,
        drive_folder_id      varchar
    );

    create table family_members
    (
        id            serial
            primary key,
        user_id       integer      not null
            references users
                on delete cascade,
        name          varchar(255) not null,
        date_of_birth date,
        created_at    timestamp default CURRENT_TIMESTAMP,
        updated_at    timestamp default CURRENT_TIMESTAMP
    );

    create index idx_family_members_user_id
        on family_members (user_id);

    create table medications
    (
        id              serial
            primary key,
        user_id         integer             not null
            references users
                on delete cascade,
        name            varchar(255)        not null,
        quantity        integer   default 0 not null,
        expiration_date date,
        created_at      timestamp default CURRENT_TIMESTAMP,
        updated_at      timestamp default CURRENT_TIMESTAMP
    );

    create index idx_medications_user_id
        on medications (user_id);

    create table medication_usage
    (
        id               serial
            primary key,
        family_member_id integer             not null
            references family_members
                on delete cascade,
        medication_id    integer             not null
            references medications
                on delete cascade,
        used_at          timestamp default CURRENT_TIMESTAMP,
        quantity_used    integer   default 1 not null,
        created_at       timestamp default CURRENT_TIMESTAMP,
        updated_at       timestamp default CURRENT_TIMESTAMP
    );

    create index idx_medication_usage_family_member_id
        on medication_usage (family_member_id);

    create index idx_medication_usage_medication_id
        on medication_usage (medication_id);

    create table user_google_credentials
    (
        id            serial
            primary key,
        user_id       integer   not null
            unique
            references users
                on delete cascade,
        access_token  text      not null,
        refresh_token text      not null,
        token_expiry  timestamp not null,
        created_at    timestamp default CURRENT_TIMESTAMP,
        updated_at    timestamp default CURRENT_TIMESTAMP
    );

    create index idx_user_google_credentials_user_id
        on user_google_credentials (user_id);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    drop table if exists user_google_credentials;
    drop table if exists medication_usage;
    drop table if exists medications;
    drop table if exists family_members;
    drop table if exists users;
    """)
