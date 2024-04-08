"""rename sex column to gender

Revision ID: 00da4983bc95
Revises: b23403c79f02
Create Date: 2024-04-08 12:57:33.330309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00da4983bc95'
down_revision: Union[str, None] = 'b23403c79f02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('receptionist', 'sex', new_column_name='gender', type_=sa.String(length=255))
    op.alter_column('therapist', 'sex', new_column_name='gender', type_=sa.String(length=255))

    pass


def downgrade() -> None:
    pass
