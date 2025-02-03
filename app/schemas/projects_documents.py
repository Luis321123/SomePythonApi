from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class ProjectDocumentBase(BaseModel):
    ceco: str = None
    document_version_uuid: Optional[UUID4] = None
    correlative:int = None
    correlative_automatic: bool = False
    

class ProjectDocumentCreate(ProjectDocumentBase):
    pass

class ProjectDocumentUpdate(ProjectDocumentBase):
    pass

class ProjectDocumentInDB(ProjectDocumentBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ProjectDocument(ProjectDocumentInDB):
    pass
