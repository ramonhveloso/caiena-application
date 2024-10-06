"""Ajust relationship in forecast model

Revision ID: e98fe0ea9953
Revises: 72e3a0287ef5
Create Date: 2024-10-05 22:23:42.910100

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e98fe0ea9953"
down_revision: Union[str, None] = "72e3a0287ef5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_forecast_weather_id", table_name="forecast_weather")
    op.drop_table("forecast_weather")
    op.drop_index("ix_current_weather_city", table_name="current_weather")
    op.drop_index("ix_current_weather_id", table_name="current_weather")
    op.drop_table("current_weather")
    op.drop_index("ix_token_blacklist_id", table_name="token_blacklist")
    op.drop_table("token_blacklist")
    op.drop_index("ix_users_chave_pix", table_name="users")
    op.drop_index("ix_users_cnpj", table_name="users")
    op.drop_index("ix_users_cpf", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_name", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('users_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("cpf", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("cnpj", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("chave_pix", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("reset_pin", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "reset_pin_expiration",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_name", "users", ["name"], unique=False)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_cpf", "users", ["cpf"], unique=True)
    op.create_index("ix_users_cnpj", "users", ["cnpj"], unique=True)
    op.create_index("ix_users_chave_pix", "users", ["chave_pix"], unique=True)
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="token_blacklist_pkey"),
    )
    op.create_index("ix_token_blacklist_id", "token_blacklist", ["id"], unique=False)
    op.create_table(
        "current_weather",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("city", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "latitude",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "longitude",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "current_temperature",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "feels_like",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "temp_min",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "temp_max",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("pressure", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("humidity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("visibility", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "wind_speed",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("wind_deg", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "wind_gust",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("cloudiness", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "weather_description", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "observation_datetime",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "sunrise", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "sunset", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="current_weather_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="current_weather_pkey"),
    )
    op.create_index("ix_current_weather_id", "current_weather", ["id"], unique=False)
    op.create_index(
        "ix_current_weather_city", "current_weather", ["city"], unique=False
    )
    op.create_table(
        "forecast_weather",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column(
            "average_temperature",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "min_temperature",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "max_temperature",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "weather_description", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "humidity",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "wind_speed",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="forecast_weather_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="forecast_weather_pkey"),
    )
    op.create_index("ix_forecast_weather_id", "forecast_weather", ["id"], unique=False)
    # ### end Alembic commands ###
