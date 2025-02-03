from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class BusinessUnitBase(BaseModel):
    name: str  | None= None 
    acronym: str = None
    active: bool = False 
    order: Optional[int] = None

class BusinessUnitCreate(BusinessUnitBase):
    pass

class BusinessUnitUpdate(BusinessUnitBase):
    pass

class BusinessUnitInDB(BusinessUnitBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True
        
class BusinessUnit(BusinessUnitInDB):
    pass
