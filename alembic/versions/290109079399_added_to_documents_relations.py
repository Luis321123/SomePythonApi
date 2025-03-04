"""added to documents relations

Revision ID: 290109079399
Revises: 3abecfed5afb
Create Date: 2024-10-27 20:08:17.905923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '290109079399'
down_revision: Union[str, None] = '3abecfed5afb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('business_unit_uuid', sa.UUID(), nullable=True))
    op.add_column('documents', sa.Column('management_area_uuid', sa.UUID(), nullable=True))
    op.add_column('documents', sa.Column('discipline_uuid', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'documents', 'disciplines', ['discipline_uuid'], ['uuid'])
    op.create_foreign_key(None, 'documents', 'business_units', ['business_unit_uuid'], ['uuid'])
    op.create_foreign_key(None, 'documents', 'managements_areas', ['management_area_uuid'], ['uuid'])
    op.drop_constraint('project_document_discipline_uuid_fkey', 'project_document', type_='foreignkey')
    op.drop_constraint('project_document_business_unit_uuid_fkey', 'project_document', type_='foreignkey')
    op.drop_constraint('project_document_management_area_uuid_fkey', 'project_document', type_='foreignkey')
    op.drop_column('project_document', 'discipline_uuid')
    op.drop_column('project_document', 'management_area_uuid')
    op.drop_column('project_document', 'business_unit_uuid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_document', sa.Column('business_unit_uuid', sa.UUID(), autoincrement=False, nullable=True))
    op.add_column('project_document', sa.Column('management_area_uuid', sa.UUID(), autoincrement=False, nullable=True))
    op.add_column('project_document', sa.Column('discipline_uuid', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('project_document_management_area_uuid_fkey', 'project_document', 'managements_areas', ['management_area_uuid'], ['uuid'])
    op.create_foreign_key('project_document_business_unit_uuid_fkey', 'project_document', 'business_units', ['business_unit_uuid'], ['uuid'])
    op.create_foreign_key('project_document_discipline_uuid_fkey', 'project_document', 'disciplines', ['discipline_uuid'], ['uuid'])
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_column('documents', 'discipline_uuid')
    op.drop_column('documents', 'management_area_uuid')
    op.drop_column('documents', 'business_unit_uuid')
    # ### end Alembic commands ###