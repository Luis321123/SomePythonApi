from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.models.BaseModel import BaseModel

class ProjectDocumentCorrelative(BaseModel):
    __tablename__ = 'project_documents_correlative'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )
    project_document_uuid = Column(UUID(200), ForeignKey('project_document.uuid'))
    correlative = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
    
    #Relaciones

    project_documents = relationship("ProjectDocument", back_populates="project_documents_correlatives")
    project_documents_correlative_logs = relationship("ProjectDocumentCorrelativeLog", back_populates="project_documents_correlatives")