from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class ManagementAreasBase(BaseModel):
    name: str | None= None
    acronym: str = None
    active: bool = False
    order: Optional[int] = None

class ManagementAreasCreate(ManagementAreasBase):
    pass

class ManagementAreasUpdate(ManagementAreasBase):
    pass

class ManagementAreasInDB(ManagementAreasBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class config:
        from_attributes = True

class ManagementAreas(ManagementAreasInDB):
    pass