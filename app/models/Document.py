from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.models.BaseModel import BaseModel

class Document(BaseModel):
    __tablename__ = 'documents'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )
    document_type_uuid = Column(UUID, ForeignKey('documents_types.uuid'))
    nro = Column(Integer)
    name = Column(String(255))
    business_unit_uuid = Column(UUID, ForeignKey('business_units.uuid'))
    management_area_uuid = Column(UUID, ForeignKey('managements_areas.uuid'))
    discipline_uuid = Column(UUID, ForeignKey('disciplines.uuid'))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
    
    document_type = relationship("DocumentType", back_populates="documents", uselist=False)
    business_unit = relationship("BusinessUnit", back_populates="documents", uselist = False)
    management_areas = relationship("ManagementArea", back_populates="documents", uselist = False)
    disciplines = relationship("Discipline", back_populates="documents", uselist = False)
    document_versions = relationship("DocumentVersion", back_populates="documents")