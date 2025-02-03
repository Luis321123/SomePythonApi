from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel



class DocumentTypeBase(BaseModel):
    name: str  | None= None 
    acronym: str = None
    active: bool = False
    order: Optional[int] = None

class DocumentTipeCreate(DocumentTypeBase):
    pass

class DocumentTypeUpdate(DocumentTypeBase):
    pass

class DocumentTypeInDB(DocumentTypeBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class DocumentType(DocumentTypeInDB):
    pass