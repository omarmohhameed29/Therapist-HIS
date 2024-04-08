"""alter sex column in patient table

Revision ID: b23403c79f02
Revises: 35a33ccbc8c3
Create Date: 2024-04-08 12:54:08.291111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b23403c79f02'
down_revision: Union[str, None] = '35a33ccbc8c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('patient', 'sex', new_column_name='gender', type_=sa.String(length=255))
    pass


def downgrade() -> None:
    pass
