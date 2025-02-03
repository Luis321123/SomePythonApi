from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.document_type import DocumentTipeCreate, DocumentTypeUpdate
from app.services.base import CRUDBase
from app.models.DocumentType import DocumentType

class DocumentTypeController(CRUDBase[DocumentType, DocumentTipeCreate, DocumentTypeUpdate]):
    async def get_document_type(self, db:Session, uuid: str = None):  
        if uuid:
            documents_type = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.deleted_at == None).first()
            if not documents_type:
                    raise HTTPException(status_code=404, detail="uuid of your document_type not found.")
            return documents_type
        else:
            return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()).order_by(self.model.name.asc()).all()

    async def get_multi_document_type(self, db: Session, *, filter: str = None):
        try:
            base_query = (db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()))
            
            if filter and filter != "null":
                search = f"%{filter}%"
                base_query = base_query.filter(self.model.name.ilike(search))
            
            results = base_query.all()
            return results
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}") 

    async def create_document_type(self, data: DocumentTipeCreate, session: Session):
        try:
            new_document_type = self.create(db=session, obj_in=data)
            return new_document_type
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    
    async def update_document_type(self, data: DocumentTypeUpdate, document_type_uuid: str, session: Session):
        try:
            document_type_current_session = await self.get_document_type(db=session, uuid=document_type_uuid)
            
            self.update(db=session, db_obj=document_type_current_session, obj_in=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        
    async def delete_document_type(self, document_type_uuid:str, session: Session):
        try:
            db_obj = {"active": False}
            document_type_current = self.get(session, document_type_uuid)
            self.update(db=session, db_obj=document_type_current, obj_in=db_obj)
            self.remove(db=session, uuid=document_type_uuid) 
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

document_type_controller=DocumentTypeController(DocumentType)