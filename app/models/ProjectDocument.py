from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class ProjectDocument(BaseModel):
    __tablename__ = 'project_document'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )
    ceco = Column(String(255))
    document_version_uuid = Column(UUID(200), ForeignKey('documents_versions.uuid'))
    correlative = Column(Integer)
    correlative_automatic = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
    
    #Relaciones 
    
    documents_version = relationship("DocumentVersion", back_populates="project_documents", uselist = False)  
    project_documents_correlatives = relationship("ProjectDocumentCorrelative", back_populates="project_documents", uselist = False)