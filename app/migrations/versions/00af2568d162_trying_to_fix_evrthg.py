"""trying to fix evrthg

Revision ID: 00af2568d162
Revises: 0359c88c0ad2
Create Date: 2025-09-09 15:49:55.193569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00af2568d162'
down_revision: Union[str, Sequence[str], None] = '0359c88c0ad2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
