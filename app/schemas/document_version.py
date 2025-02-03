from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from app.schemas.file import FileSummary


class DocumentVersionBase(BaseModel):
    document_uuid: Optional[UUID4] = None
    file_uuid: Optional[UUID4] = None
    nro:  Optional[str]  = None

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersionUpdate(DocumentVersionBase):
    pass

class DocumentVersionInDB(DocumentVersionBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class Documents(DocumentVersionInDB):
    pass

class DocumentVersionsWithRelations(DocumentVersionInDB):
    file: Optional[FileSummary] = None