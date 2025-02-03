from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from app.schemas.file import FileSummary


class ProjectDocumentCorrelativeLogBase(BaseModel):
    project_document_correlative_uuid: Optional[UUID4] = None
    file_uuid: Optional[UUID4] = None
    upload_at: Optional[datetime] = None 
    upload_by: Optional[str] = None
    status: Optional[bool] = None
    status_by: Optional[str] = None
    status_at: Optional[datetime] = None
    status_comment: Optional[str] = None

class ProjectDocumentCorrelativeLogCreate(ProjectDocumentCorrelativeLogBase):
    pass

class ProjectDocumentCorrelativeLogUpdate(ProjectDocumentCorrelativeLogBase):
    pass

class ProjectDocumentCorrelativeLogInDB(ProjectDocumentCorrelativeLogBase):
    uuid: UUID4
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ProjectDocumentCorrelativeLog(ProjectDocumentCorrelativeLogInDB):
    pass

class ProjectDocumentCorrelativeLogWithRelations(ProjectDocumentCorrelativeLogInDB):
    file: Optional[FileSummary] = None