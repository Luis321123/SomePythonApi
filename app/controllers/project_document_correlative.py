from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, UploadFile

from app.schemas.project_document_correlative import ProjectDocumentCorrelativeCreate, ProjectDocumentCorrelativeUpdate
from app.services.base import CRUDBase
from app.models.ProjectDocumentCorrelative import ProjectDocumentCorrelative
from app.controllers.files import file_controller
from app.utils.files import supported_img_filetypes, supported_document_filetypes

class ProjectDocumentCorrelativeController(CRUDBase[ProjectDocumentCorrelative, ProjectDocumentCorrelativeCreate, ProjectDocumentCorrelativeUpdate]):
    async def get_project_document_correlative(self, db: Session, uuid: str = None, include_deleted: bool = False):
        if uuid:
            project_document_correlative = db.query(self.model).filter(self.model.uuid == uuid).first()
            if not project_document_correlative or (not include_deleted and project_document_correlative.deleted_at is not None):
                raise HTTPException(status_code=404, detail="UUID of your project_document_correlative not found.")
            return project_document_correlative
        else:
            if include_deleted:
                return db.query(self.model).filter(self.model.deleted_at.isnot(None)).order_by(self.model.correlative.asc()).all()
            else:
                return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.correlative.asc()).all()
                
    async def get_multi_project_document_correlative(self, db: Session, *, project_document_uuid: str):
        try:
            base_query = db.query(self.model).where(self.model.deleted_at == None).order_by(self.model.correlative.asc())
            if project_document_uuid is not None and project_document_uuid != "null":
                query_search = base_query.filter(self.model.project_document_uuid == project_document_uuid)
            else:
                query_search = base_query
            return query_search.all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")  

    async def create_projec_document_correlative(self,data: ProjectDocumentCorrelativeCreate,session: Session):
        try:
            document = self.create(db=session, obj_in=data)
            return document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def update_projec_document_correlative(self, data: ProjectDocumentCorrelativeUpdate, document_correlative_uuid: str, session: Session, file: Optional[UploadFile] | None, upload_by: str = None, user_uuid: str = None):    
        try:
            document_correlative_current = await self.get_project_document_correlative(db=session, uuid=document_correlative_uuid)
            
            if file:
                file_extension = file.filename.split('.')[-1].lower()
                if file_extension in supported_img_filetypes:
                    supported_file_type = 'images'
                elif file_extension in supported_document_filetypes:
                    supported_file_type = 'documents'
                else:
                    raise HTTPException(status_code=400, detail="File type not supported.")
            
                uploaded_file = await file_controller.upload_file(file=file, comment="Project Document Correlative file update", db=session, user_uuid=user_uuid, supported_file=supported_file_type )                
                document_correlative_current.file_uuid = uploaded_file.uuid
                document_correlative_current.upload_by = upload_by
                document_correlative_current.upload_at = datetime.utcnow()            
            if data.correlative is not None:
                if data.correlative != 0:
                    document_correlative_current.correlative = data.correlative
            document_update = self.update(db=session, db_obj=document_correlative_current, obj_in=data)
            
            return document_update, document_correlative_current.file.path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")

    async def delete_project_document_correlative(self, project_document_correlative_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=project_document_correlative_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
 
project_document_correlative_controller=ProjectDocumentCorrelativeController(ProjectDocumentCorrelative)

