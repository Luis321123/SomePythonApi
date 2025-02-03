from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, UploadFile

from app.schemas.project_document_correlative_logs import ProjectDocumentCorrelativeLogCreate, ProjectDocumentCorrelativeLogUpdate
from app.services.base import CRUDBase
from app.models.ProjectDocumentCorrelativeLogs import ProjectDocumentCorrelativeLog
from app.controllers.files import file_controller
from app.utils.files import supported_img_filetypes, supported_document_filetypes


class ProjectDocumentCorrelativeLogController(CRUDBase[ProjectDocumentCorrelativeLog, ProjectDocumentCorrelativeLogCreate, ProjectDocumentCorrelativeLogUpdate]):
    async def get_project_document_correlative_logs(self, db: Session, project_document_correlative_uuid: str = None, include_deleted: bool = False):
        if project_document_correlative_uuid:
            query = db.query(self.model).filter(
                (self.model.project_document_correlative_uuid == project_document_correlative_uuid) |
                (self.model.project_document_correlative_uuid.is_(None))).order_by(self.model.project_document_correlative_uuid == project_document_correlative_uuid,self.model.status.asc())
            return query.all()
        else:
            if include_deleted:
                return db.query(self.model).filter(self.model.deleted_at.isnot(None)).order_by(self.model.status.asc()).all()
            else:
                return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.status.asc()).all()
            
    async def get_project_document_correlative_log_by_uuid(self, db: Session, project_document_correlative_log_uuid: str):
        result = db.query(self.model).filter(self.model.uuid == project_document_correlative_log_uuid).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return result
                
    async def get_multi_project_document_correlative_logs(self, db: Session, *, project_document_uuid: str):
        try:
            base_query = db.query(self.model).where(self.model.deleted_at == None).options(joinedload(self.model.file)).order_by(self.model.correlative.asc())
            if project_document_uuid is not None and project_document_uuid != "null":
                query_search = base_query.filter(self.model.project_document_uuid == project_document_uuid)
            else:
                query_search = base_query
            return query_search.all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")  

    async def create_projec_document_correlative_logs(self, data: ProjectDocumentCorrelativeLogCreate, session: Session, user_name: str,file: UploadFile | None):
        try:
            print(type(data))  

            if file:
                file_extension = file.filename.split('.')[-1].lower() 
                if file_extension in supported_img_filetypes:
                    supported_file_type = 'images'
                elif file_extension in supported_document_filetypes:
                    supported_file_type = 'documents'
                else:
                    raise HTTPException(status_code=400, detail="File type not supported.")
                
                uploaded_file = await file_controller.upload_file(file=file, comment="Correlative document file upload", db=session, user_uuid=user_name, supported_file=supported_file_type)
                data.file_uuid = uploaded_file.uuid 
                data.upload_by = user_name  #
                data.upload_at = datetime.utcnow()
            document_version = self.create(db=session, obj_in=data) 
            return document_version, uploaded_file.path if file else None

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear el project_document_correlative: {str(e)} - Tipo de data: {type(data)}")
                    
    async def update_project_document_correlative_status(self, document_correlative_uuid: str, status: Optional[bool], session: Session, user_name: str, status_comment:Optional[str] = None  ):
        try:
            document_correlative_current = await self.get_project_document_correlative_log_by_uuid(db=session, project_document_correlative_log_uuid=document_correlative_uuid)

            if status not in {None, True, False}:
                raise HTTPException(status_code=400, detail="Status inválido. Debe ser True, False o None.")

            document_correlative_current.status = status
            document_correlative_current.status_by = user_name 
            document_correlative_current.status_at = datetime.utcnow()
            document_correlative_current.status_comment = status_comment

            session.commit()
            session.refresh(document_correlative_current)
            return document_correlative_current

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")

    async def delete_project_document_correlative_logs(self, project_document_correlative_log_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=project_document_correlative_log_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
            
project_document_correlative_log_controller=ProjectDocumentCorrelativeLogController(ProjectDocumentCorrelativeLog)

