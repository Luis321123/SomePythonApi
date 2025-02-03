from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.management_areas import ManagementAreasCreate, ManagementAreasUpdate
from app.services.base import CRUDBase
from app.models.ManagementAreas import ManagementArea

class ManagementAreaController(CRUDBase[ManagementArea, ManagementAreasCreate, ManagementAreasUpdate]):
    async def get_management_area(self, db:Session, uuid: str = None):
        if uuid:
            management_areas = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.deleted_at == None).order_by(self.model.acronym.asc()).first()
            if not management_areas:
                    raise HTTPException(status_code=404, detail="uuid of management_area not found.")
            return management_areas
        else:
            return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()).order_by(self.model.acronym.asc()).all()
        
    async def get_multi_management_area(self, db: Session, *, filter: str = None):
        try:
            base_query = (db.query(self.model).filter(self.model.deleted_at == None).filter(self.model.active == True).order_by(self.model.name.asc()))
            
            if filter and filter != "null":
                search = f"%{filter}%"
                base_query = base_query.filter(self.model.name.ilike(search))
            
            results = base_query.all()
            return results
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")

    async def create_management_area(self, data: ManagementAreasCreate, session: Session):
        try:
            management_area_current = self.create(db=session, obj_in=data)
            return management_area_current
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def update_management_area(self, data: ManagementAreasUpdate, management_area_uuid: str, session: Session):
        try:
            management_area_current = await self.get_management_area(db=session, uuid=management_area_uuid)
            
            self.update(db=session, db_obj=management_area_current, obj_in=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def delete_management_area(self, management_area_uuid:str, session: Session):
        try:
            db_obj = {"active": False}
            discipline_current = self.get(session, management_area_uuid)
            self.update(db=session, db_obj=discipline_current, obj_in=db_obj)
            self.remove(db=session, uuid=management_area_uuid)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

management_area_controller=ManagementAreaController(ManagementArea)