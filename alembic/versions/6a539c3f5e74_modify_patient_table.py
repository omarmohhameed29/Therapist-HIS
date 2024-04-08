"""modify patient table

Revision ID: 6a539c3f5e74
Revises: 
Create Date: 2024-04-08 12:39:42.777290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a539c3f5e74'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("test", sa.Column('id', sa.Integer(), primary_key=True, nullable=False))
    pass


def downgrade() -> None:
    pass
