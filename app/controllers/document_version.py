
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, UploadFile

from app.schemas.document_version import DocumentVersionCreate, DocumentVersionUpdate
from app.services.base import CRUDBase
from app.models.DocumentVersion import DocumentVersion
from app.controllers.files import file_controller


class DocumentVersionController(CRUDBase[DocumentVersion, DocumentVersionCreate, DocumentVersionUpdate]):
    async def get_document_version(self, db:Session, uuid: str = None, document_uuid:str = None):  
        if uuid:
            documents_versions = db.query(DocumentVersion).filter(DocumentVersion.uuid == uuid).filter(DocumentVersion.deleted_at == None).first()

            if not documents_versions:
                    raise HTTPException(status_code=404, detail="uuid of document_version not found.")
            return documents_versions
        else:
            query = db.query(self.model).filter(self.model.deleted_at == None).options(joinedload(self.model.file)).order_by(self.model.nro.asc())

        if document_uuid:
            
            query = query.filter(self.model.document_uuid == document_uuid)
        return query.all()

    async def create_document_version(self, data: DocumentVersionCreate, file: Optional[UploadFile] | None, session: Session, user_uuid: str):
        try:
            if file:
                file_extension = file.filename.split('.')[-1].lower()
                supported_img_filetypes = ['jpg', 'jpeg', 'png', 'gif']
                supported_document_filetypes = ['pdf', 'doc', 'docx']

                if file_extension in supported_img_filetypes:
                    supported_file_type = 'images'
                elif file_extension in supported_document_filetypes:
                    supported_file_type = 'documents'
                else:
                    raise HTTPException(status_code=400, detail="File type not supported.")
                
                uploaded_file = await file_controller.upload_file(file=file, comment="Document version file upload", db=session, user_uuid=user_uuid, supported_file=supported_file_type)
                data.file_uuid = uploaded_file.uuid
            
            document_versions = self.create(db=session, obj_in=data)
            
            return document_versions
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear la versión del documento: {str(e)}")
    
    async def update_document_version(self,data: DocumentVersionUpdate,document_version_uuid: str,session: Session,file: Optional[UploadFile] = None,user_uuid: str = None):
        try:
            document_version_current = await self.get_document_version(db=session, uuid=document_version_uuid)

            if file:
                document_version_current.deleted_at = datetime.utcnow()
                self.update(db=session, db_obj=document_version_current, obj_in={})

                uploaded_file = await file_controller.upload_file(file=file,comment="Actualización de document_version",db=session,user_uuid=user_uuid,supported_file='documents')

                new_document_version = DocumentVersion(document_uuid=document_version_current.document_uuid,file_uuid=uploaded_file.uuid,
                    nro=data.nro if data.nro is not None else document_version_current.nro,
                    created_at=datetime.utcnow(),)
                
                self.create(db=session, obj_in=new_document_version)
                return new_document_version, uploaded_file.path

            if data.document_uuid is not None:
                document_version_current.document_uuid = data.document_uuid

            if data.nro is not None:
                document_version_current.nro = data.nro


            document_update = self.update(db=session, db_obj=document_version_current, obj_in=data)

            return document_update, document_update.file.path if document_version_current.file_uuid else None

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar la versión del documento: {str(e)}")

    async def delete_document_version(self, document_version_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=document_version_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

document_version_controller=DocumentVersionController(DocumentVersion)