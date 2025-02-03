from uuid import uuid4
from sqlalchemy import Column, DateTime, String ,Integer,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class File_tb(BaseModel):
    __tablename__ = 'files'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )

    name = Column(String(50))
    comment = Column(String(255))
    path = Column(String(150))
    ext = Column(String(50))
    size = Column(Integer)
    folder = Column(String(20))
    created_by = Column(String(125), index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)

    document_version = relationship("DocumentVersion", back_populates="file")
    project_documents_correlatives_logs = relationship("ProjectDocumentCorrelativeLog", back_populates="file")