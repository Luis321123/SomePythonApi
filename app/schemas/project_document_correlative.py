from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel



class ProjectDocumentCorrelativeBase(BaseModel):
    project_document_uuid: Optional[UUID4] = None
    correlative: Optional[int] = None

class ProjectDocumentCorrelativeCreate(ProjectDocumentCorrelativeBase):
    pass

class ProjectDocumentCorrelativeUpdate(ProjectDocumentCorrelativeBase):
    pass

class ProjectDocumentCorrelativeInDB(ProjectDocumentCorrelativeBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ProjectDocumentCorrelative(ProjectDocumentCorrelativeInDB):
    pass
