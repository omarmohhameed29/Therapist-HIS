"""empty message

Revision ID: 35a33ccbc8c3
Revises: 6a539c3f5e74
Create Date: 2024-04-08 12:46:53.712346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35a33ccbc8c3'
down_revision: Union[str, None] = '6a539c3f5e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("test")
    pass


def downgrade() -> None:
    pass
