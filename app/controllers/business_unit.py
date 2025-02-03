from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.business_unit import BusinessUnitCreate, BusinessUnitUpdate
from app.services.base import CRUDBase
from app.models.BusinessUnit import BusinessUnit

class BusinessUnitController(CRUDBase[BusinessUnit, BusinessUnitCreate, BusinessUnitUpdate]):
    async def get_business_unit(self, db: Session, uuid: str = None):
        if uuid:
            business_unit = db.query(self.model).filter(self.model.uuid == uuid).order_by(self.model.name.asc()).first()
            if not business_unit:
                raise HTTPException(status_code=404, detail="uuid business_unit not found.")
            return business_unit
        else:
            return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()).order_by(self.model.name.asc()).all()

    async def create_business_unit(self, data: BusinessUnitCreate, session: Session):
        try:
            unit = self.create(db=session, obj_in=data)
            return unit
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def update_business_unit(self, data: BusinessUnitUpdate, business_unit_uuid: str, session: Session):
        try:
            business_unit_current = await self.get_business_unit(db=session, uuid=business_unit_uuid)
            
            self.update(db=session, db_obj=business_unit_current, obj_in=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        
    async def delete_business_unit(self, business_unit_uuid:str, session: Session):
        try:
            db_obj = {"active": False}
            business_current = self.get(session, business_unit_uuid)
            self.update(db=session, db_obj=business_current, obj_in=db_obj)
            self.remove(db=session, uuid=business_unit_uuid)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

Business_unit=BusinessUnitController(BusinessUnit)