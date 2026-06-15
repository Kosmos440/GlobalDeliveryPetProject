"""fix package numeric column types

Revision ID: a1b2c3d4e5f6
Revises: bc73b24bfef3
Create Date: 2026-06-14 14:30:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "bc73b24bfef3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "packages",
        "weight",
        existing_type=sa.Integer(),
        type_=sa.Numeric(10, 3),
        postgresql_using="weight::numeric(10,3)",
        existing_nullable=False,
    )
    op.alter_column(
        "packages",
        "value_usd",
        existing_type=sa.Integer(),
        type_=sa.Numeric(12, 2),
        postgresql_using="value_usd::numeric(12,2)",
        existing_nullable=True,
    )
    op.alter_column(
        "packages",
        "delivery_cost_rub",
        existing_type=sa.Integer(),
        type_=sa.Numeric(12, 2),
        postgresql_using="delivery_cost_rub::numeric(12,2)",
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "packages",
        "delivery_cost_rub",
        existing_type=sa.Numeric(12, 2),
        type_=sa.Integer(),
        postgresql_using="delivery_cost_rub::integer",
        existing_nullable=True,
    )
    op.alter_column(
        "packages",
        "value_usd",
        existing_type=sa.Numeric(12, 2),
        type_=sa.Integer(),
        postgresql_using="value_usd::integer",
        existing_nullable=True,
    )
    op.alter_column(
        "packages",
        "weight",
        existing_type=sa.Numeric(10, 3),
        type_=sa.Integer(),
        postgresql_using="weight::integer",
        existing_nullable=False,
    )
