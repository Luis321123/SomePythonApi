from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.models.BaseModel import BaseModel

class ProjectDocumentCorrelativeLog(BaseModel):
    __tablename__ = 'project_documents_correlative_logs'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )
    project_document_correlative_uuid = Column(UUID(200), ForeignKey('project_documents_correlative.uuid'))
    file_uuid =  Column(UUID(200), ForeignKey('files.uuid'), nullable=True)
    upload_by = Column(String(255), nullable=True)
    upload_at= Column(DateTime, nullable=True)
    status= Column(Boolean, nullable=True)
    status_by = Column(String(255), nullable=True)
    status_at= Column(DateTime, nullable=True)
    status_comment = Column(String(255), nullable=True)

    deleted_at = Column(DateTime, nullable=True, default=None)
    
    #Relaciones

    project_documents_correlatives = relationship("ProjectDocumentCorrelative", back_populates="project_documents_correlative_logs")
    file = relationship("File_tb", back_populates= "project_documents_correlatives_logs")