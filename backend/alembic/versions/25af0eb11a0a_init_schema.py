"""init schema

Revision ID: 25af0eb11a0a
Revises: 26b1e8b640ca
Create Date: 2025-10-31 19:55:51.728826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25af0eb11a0a'
down_revision: Union[str, None] = '26b1e8b640ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
