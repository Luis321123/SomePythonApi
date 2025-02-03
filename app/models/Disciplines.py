from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ARRAY
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class Discipline(BaseModel):
    __tablename__ = 'disciplines'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )   
    name = Column(String(255))
    acronym = Column(String(3))
    active = Column(Boolean, default=False)
    order = Column(Integer, nullable=True)
    business_unit_uuid = Column(ARRAY(UUID), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)

    #Relaciones

    documents = relationship("Document", back_populates="disciplines")
