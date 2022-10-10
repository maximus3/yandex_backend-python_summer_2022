"""empty message

Revision ID: 5d94548d7632
Revises: 7a52f33acae9
Create Date: 2022-08-10 22:09:45.463566

"""
from pathlib import Path

from alembic import op
import sqlalchemy as sa
import csv


# revision identifiers, used by Alembic.
revision = '5d94548d7632'
down_revision = '7a52f33acae9'
branch_labels = None
depends_on = None


BASE_DIR = Path(__file__).parent.parent.parent.parent.parent.resolve()
FILL_ORDER = (
    'spaceship_manufacturer',
    'spaceship_model',
    'spaceship',
    'driver',
    'spaceship_rent',
)
DIR_WITH_DATA = BASE_DIR / 'migrations/init_data'


def upgrade() -> None:
    for table_name in FILL_ORDER:
        filename = DIR_WITH_DATA / f'{table_name}.csv'
        if not filename.exists():
            continue
        with open(filename) as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
            columns = []
            for i, row in enumerate(datareader):
                if i == 0:
                    columns = row
                    continue
                op.execute('''
                    INSERT INTO {table_name} ({columns})
                    VALUES ({values})
                    '''.format(
                        table_name=table_name,
                        columns=', '.join(columns),
                        values=', '.join(map(lambda value: f"\'{str(value)}\'", row)),
                    ))


def downgrade() -> None:
    for table_name in FILL_ORDER[::-1]:
        op.execute(f'DELETE FROM {table_name}')
