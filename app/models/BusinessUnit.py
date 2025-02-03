from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime , Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.models.BaseModel import BaseModel

class BusinessUnit(BaseModel):
    __tablename__ = 'business_units'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )
    name = Column(String(255))
    acronym = Column(String(3))
    active = Column(Boolean, default=False)
    order = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)

    #Relaciones

    documents = relationship("Document", back_populates="business_unit")