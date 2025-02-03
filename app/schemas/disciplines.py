from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class DisciplinesBase(BaseModel):
    name: str  | None= None 
    acronym: str = None
    active: bool = False 
    order: Optional[int] = None
    business_unit_uuid: Optional[list[UUID4]] = None

class DisciplinesCreate(DisciplinesBase):
    pass

class DisciplinesUpdate(DisciplinesBase):
    pass

class DisciplinesInDB(DisciplinesBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class Disciplines(DisciplinesInDB):
    pass