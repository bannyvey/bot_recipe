"""creating_categories

Revision ID: 146db5c4dc54
Revises: a3c805ef58f3
Create Date: 2025-11-12 11:24:57.992014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from v2.utils.constants import CATEGORY_MAPPING

# revision identifiers, used by Alembic.
revision: str = '146db5c4dc54'
down_revision: Union[str, None] = 'a3c805ef58f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    categories_tabel = sa.table(
        'categories',
        sa.column('name', sa.String()),
        sa.column('description', sa.String())
    )
    categories_data = [
    {'name': key,  'description': ""}
    for key in CATEGORY_MAPPING.keys()
]

    op.bulk_insert(categories_tabel, categories_data)

def downgrade() -> None:
    names = tuple(key for key in CATEGORY_MAPPING.keys())
    op.execute(
        sa.delete(sa.table('categories')).where(sa.column('name').in_(names))
    )
