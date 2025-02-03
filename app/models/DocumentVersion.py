from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class DocumentVersion(BaseModel):
    __tablename__ = 'documents_versions'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )

    file_uuid = Column(UUID(200), ForeignKey('files.uuid'), nullable=True)
    document_uuid = Column(UUID(200), ForeignKey('documents.uuid'))
    nro = Column(String(255))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
    
    #Relaciones    

    file = relationship("File_tb", back_populates="document_version", uselist = False)
    project_documents = relationship("ProjectDocument", back_populates="documents_version")
    documents = relationship("Document", back_populates="document_versions", uselist = False)
