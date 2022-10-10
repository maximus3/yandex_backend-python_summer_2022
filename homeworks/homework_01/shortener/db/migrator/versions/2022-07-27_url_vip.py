"""empty message

Revision ID: 7775a2acf09e
Revises: 970d84738c0b
Create Date: 2022-07-27 21:40:38.420621

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "7775a2acf09e"
down_revision = "970d84738c0b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("url_storage", sa.Column("is_vip", sa.BOOLEAN(), nullable=False))
    op.add_column("url_storage", sa.Column("dt_expiration", postgresql.TIMESTAMP(timezone=True), nullable=True))
    op.drop_constraint("uq__url_storage__long_url", "url_storage", type_="unique")
    op.drop_constraint("uq__url_storage__short_url", "url_storage", type_="unique")
    op.drop_index("ix__url_storage__long_url", table_name="url_storage")
    op.create_index(op.f("ix__url_storage__long_url"), "url_storage", ["long_url"], unique=False)
    op.create_unique_constraint(op.f("uq__url_storage__number_of_clicks"), "url_storage", ["number_of_clicks"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq__url_storage__number_of_clicks"), "url_storage", type_="unique")
    op.drop_index(op.f("ix__url_storage__long_url"), table_name="url_storage")
    op.create_index("ix__url_storage__long_url", "url_storage", ["long_url"], unique=False)
    op.create_unique_constraint("uq__url_storage__short_url", "url_storage", ["short_url"])
    op.create_unique_constraint("uq__url_storage__long_url", "url_storage", ["long_url"])
    op.drop_column("url_storage", "dt_expiration")
    op.drop_column("url_storage", "is_vip")
    # ### end Alembic commands ###