"""Creación de tabla 123123123

Revision ID: 4cf0fc40db9b
Revises: d644f51f6135
Create Date: 2024-10-25 18:37:48.094885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cf0fc40db9b'
down_revision: Union[str, None] = 'd644f51f6135'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verificar si la columna 'order' no existe en 'documents_types' antes de agregarla
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'documents_types' AND column_name = 'order') THEN
                ALTER TABLE documents_types ADD COLUMN "order" INTEGER;
            END IF;
        END $$;
    """)


def downgrade() -> None:
    # Eliminar la columna 'order' en caso de ser necesario
    op.drop_column('documents_types', 'order')