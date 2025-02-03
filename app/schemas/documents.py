from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class DocumentsBase(BaseModel):
    document_type_uuid: Optional[UUID4] = None
    name: str = None 
    nro: int = None
    business_unit_uuid: Optional[UUID4] = None
    management_area_uuid: Optional[UUID4] = None
    discipline_uuid: Optional[UUID4] = None

class DocumentsCreate(DocumentsBase):
    pass

class DocumentsUpdate(DocumentsBase):
    pass

class DocumentsIndDb(DocumentsBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class Documents(DocumentsIndDb):
    pass