"""empty message

Revision ID: 7a52f33acae9
Revises: 
Create Date: 2022-08-10 21:48:38.146800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a52f33acae9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'spaceship_manufacturer',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('company_name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('country', sa.VARCHAR(length=50)),
        sa.Column('nasdaq_code', sa.VARCHAR(length=50)),
    )
    op.create_table(
        'spaceship_model',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('manufacturer_id', sa.Integer(), sa.ForeignKey('spaceship_manufacturer.id'), nullable=False),
        sa.Column('model_name', sa.VARCHAR(length=50)),
        sa.Column('horsepower', sa.Float(), sa.Sequence('horsepower_seq', minvalue=170000000, maxvalue=240000000), nullable=False),
        sa.CheckConstraint('horsepower >= 170000000 AND horsepower <= 240000000', name='horsepower_constraint'),
    )
    op.create_table(
        'spaceship',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('ship_number', sa.VARCHAR(50), nullable=False),
        sa.Column('model_id', sa.Integer(), sa.ForeignKey('spaceship_model.id'), nullable=False),
    )
    op.create_table(
        'driver',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.VARCHAR(50), nullable=False),
        sa.Column('last_name', sa.VARCHAR(50)),
        sa.Column('login', sa.VARCHAR(50), unique=True, nullable=False),
        sa.Column('city', sa.VARCHAR(30)),
    )
    op.create_table(
        'spaceship_rent',
        sa.Column('driver_id', sa.Integer(), sa.ForeignKey('driver.id'), nullable=False),
        sa.Column('spaceship_id', sa.Integer(), sa.ForeignKey('spaceship.id'), nullable=False),
        sa.Column('rent_start', sa.TIMESTAMP(), nullable=False),
        sa.Column('rent_end', sa.TIMESTAMP(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('spaceship_rent')
    op.drop_table('driver')
    op.drop_table('spaceship')
    op.drop_table('spaceship_model')
    op.drop_table('spaceship_manufacturer')
