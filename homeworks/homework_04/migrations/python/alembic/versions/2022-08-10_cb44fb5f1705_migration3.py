"""empty message

Revision ID: cb44fb5f1705
Revises: 5d94548d7632
Create Date: 2022-08-10 22:34:03.136850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb44fb5f1705'
down_revision = '5d94548d7632'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'driver',
        sa.Column('full_name', sa.VARCHAR(255)),
    )
    op.execute("UPDATE driver SET full_name = CONCAT(name, ' ', last_name)")
    op.alter_column('driver', 'full_name', nullable=False)
    op.drop_column('driver', 'name')
    op.drop_column('driver', 'last_name')

    op.add_column(
        'spaceship_manufacturer',
        sa.Column('moex_code', sa.VARCHAR(50)),
    )
    op.execute("UPDATE spaceship_manufacturer SET moex_code = CONCAT(nasdaq_code, '_ru')")
    op.drop_column('spaceship_manufacturer', 'nasdaq_code')


def downgrade() -> None:
    op.add_column(
        'driver',
        sa.Column('name', sa.VARCHAR(50)),
    )
    op.add_column(
        'driver',
        sa.Column('last_name', sa.VARCHAR(50)),
    )
    op.execute("UPDATE driver SET name = SPLIT_PART(full_name, ' ', 1), last_name = SPLIT_PART(full_name, ' ', 2)")
    op.alter_column('driver', 'name', nullable=False)
    op.drop_column('driver', 'full_name')

    op.add_column(
        'spaceship_manufacturer',
        sa.Column('nasdaq_code', sa.VARCHAR(50)),
    )
    op.execute("UPDATE spaceship_manufacturer SET nasdaq_code = SPLIT_PART(moex_code, '_', 1)")
    op.drop_column('spaceship_manufacturer', 'moex_code')
