"""add contents column to posts table

Revision ID: 886b32390db2
Revises: 1af776a869aa
Create Date: 2026-06-15 18:43:09.558357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '886b32390db2'
down_revision: Union[str, Sequence[str], None] = '1af776a869aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("contents", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
