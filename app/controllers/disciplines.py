from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.disciplines import DisciplinesCreate, DisciplinesUpdate
from app.services.base import CRUDBase
from app.models.Disciplines import Discipline

class DisciplineController(CRUDBase[Discipline, DisciplinesCreate, DisciplinesUpdate]):
    async def get_discipline(self, db: Session, uuid: Optional[str] = None, business_unit_uuid: Optional[str] = None):
        query = db.query(self.model).filter(self.model.deleted_at == None)
        if uuid:
            discipline = query.filter(self.model.uuid == uuid).first()
            if not discipline:
                raise HTTPException(status_code=404, detail="UUID discipline not found.")
            return discipline

        if business_unit_uuid:
            query = query.filter(
                (self.model.business_unit_uuid == business_unit_uuid) |
                (self.model.business_unit_uuid.is_(None))
            ).order_by(
                self.model.business_unit_uuid == business_unit_uuid,  
                self.model.name.asc(),
                self.model.order.asc())
        return query.all()

    async def get_multi_disciplines(self, db: Session, *, filter: str = None, business_unit_uuid: str = None):
        try:
            base_query = (db.query(self.model).filter(self.model.deleted_at == None).filter(self.model.active == True).order_by(self.model.name.asc()))
            
            if filter and filter != "null":
                search = f"%{filter}%"
                base_query = base_query.filter(self.model.name.ilike(search))
            
            if business_unit_uuid:
                base_query = base_query.filter(self.model.business_unit_uuid.any(business_unit_uuid))
            
            results = base_query.all()
            return results
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")

    async def create_discipline(self, data: DisciplinesCreate, session: Session):
        try:
            discipline = self.create(db=session, obj_in=data)

            if data.business_unit_uuid: 
                discipline.business_unit_uuid = data.business_unit_uuid
            
            session.add(discipline)
            session.commit()
            session.refresh(discipline)

            return discipline  
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")
        
    async def update_discipline(self, data: DisciplinesUpdate, disciplines_uuid: str, session: Session):
        try:
            discipline_current = await self.get_discipline(db=session, uuid=disciplines_uuid)
            
            updating = self.update(db=session, db_obj=discipline_current, obj_in=data)
            return updating
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        
    async def delete_discipline(self, disciplines_uuid:str, session: Session):
        try:
            db_obj = {"active": False}
            discipline_current = self.get(session, disciplines_uuid)
            self.update(db=session, db_obj=discipline_current, obj_in=db_obj)
            self.remove(db=session, uuid=disciplines_uuid)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

discipline_controller=DisciplineController(Discipline)