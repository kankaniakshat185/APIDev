"""add posts & users foreign key

Revision ID: 9e4ebf9db56b
Revises: 821e11c30d5c
Create Date: 2026-06-15 19:34:23.063636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4ebf9db56b'
down_revision: Union[str, Sequence[str], None] = '821e11c30d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        'post_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )

    pass


def downgrade():
    op.drop_constraint(
        'post_users_fk',
        table_name='posts'
    )

    op.drop_column(
        'posts',
        'owner_id'
    )

    pass
