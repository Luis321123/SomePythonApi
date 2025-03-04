"""Creación de columnas

Revision ID: 4d377b866d5a
Revises: 32675ce03817
Create Date: 2024-10-18 20:45:56.634556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d377b866d5a'
down_revision: Union[str, None] = '32675ce03817'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_documents_correlative', sa.Column('upload_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_documents_correlative', 'upload_at')
    # ### end Alembic commands ###