from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.ProjectDocumentCorrelative import ProjectDocumentCorrelative
from app.models.ProjectDocumentCorrelativeLogs import ProjectDocumentCorrelativeLog
from app.schemas.project_document_correlative import ProjectDocumentCorrelativeCreate
from app.schemas.projects_documents import ProjectDocumentCreate, ProjectDocumentUpdate
from app.services.base import CRUDBase
from app.models.ProjectDocument import ProjectDocument
from app.controllers.project_document_correlative import project_document_correlative_controller

class ProjectDocumentController(CRUDBase[ProjectDocument, ProjectDocumentCreate, ProjectDocumentUpdate]):
    async def get_project_document(self, db:Session, uuid: str = None, project_document_uuid:str = None):
        if uuid:
            documents_versions = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.deleted_at == None).first()
            if not documents_versions:
                    raise HTTPException(status_code=404, detail="uuid of document_project not found.")
            return documents_versions
        query = db.query(ProjectDocument).filter(ProjectDocument.deleted_at == None).order_by(ProjectDocument.correlative.asc())
        if project_document_uuid:
            query = query.filter(ProjectDocument.uuid == project_document_uuid)
        return query.all()

    async def create_project_document(self, data: ProjectDocumentCreate, session: Session):
        try:
            existing_document = session.query(ProjectDocument).filter(
                ProjectDocument.ceco == data.ceco,
                ProjectDocument.document_version_uuid == data.document_version_uuid).first()

            if existing_document:
                raise HTTPException(status_code=400, detail="Ya existe un documento con el mismo 'ceco' y 'document_version'.")

            project_document = self.create(db=session, obj_in=data)
            correlatives_created = []

            if data.correlative_automatic and data.correlative is not None:
                for i in range(1, data.correlative + 1):
                    correlative_data = ProjectDocumentCorrelativeCreate(project_document_uuid=project_document.uuid,correlative=i,)
                    correlative = await project_document_correlative_controller.create_projec_document_correlative(data=correlative_data, session=session)
                    correlatives_created.append(correlative)

            return {
                "project_document": {
                    "uuid": project_document.uuid,
                    "ceco": project_document.ceco,
                    "correlative": project_document.correlative,
                    "document_version_uuid": project_document.document_version_uuid,
                    "created_at": project_document.created_at,
                },
                "correlatives": correlatives_created
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")
        
    async def search_project_document(self, db: Session, ceco: str = None, document_version_uuid: str = None):
        try:
            query = db.query(self.model).filter(self.model.deleted_at == None)

            if ceco is not None:
                query = query.filter(self.model.ceco == ceco)

            if document_version_uuid is not None:
                query = query.filter(self.model.document_version_uuid == document_version_uuid)

            results = query.all()

            if not results:
                raise HTTPException(status_code=404, detail="No project documents found.")

            return results
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    async def update_project_document(self, data: ProjectDocumentUpdate, project_document_uuid: str, session: Session):
        try:
            project_document_current = await self.get_project_document(db=session, uuid=project_document_uuid)

            if not project_document_current:
                raise HTTPException(status_code=404, detail="Project document not found")

            if data.correlative is not None:
                current_correlative_count = project_document_current.correlative

                if data.correlative > current_correlative_count:
                    for new_correlative in range(current_correlative_count + 1, data.correlative + 1):
                        new_correlative_record = ProjectDocumentCorrelative(project_document_uuid=project_document_uuid,correlative=new_correlative,created_at=datetime.utcnow(),)
                        session.add(new_correlative_record)
                    session.commit()
                    print(f"Created {data.correlative - current_correlative_count} new correlatives.")

                elif data.correlative < current_correlative_count:
                    correlatives_to_delete = session.query(ProjectDocumentCorrelative).filter(ProjectDocumentCorrelative.project_document_uuid == project_document_uuid,ProjectDocumentCorrelative.correlative > data.correlative).all()

                    for correlative in correlatives_to_delete:
                        correlatives_logs = session.query(ProjectDocumentCorrelativeLog).filter(ProjectDocumentCorrelativeLog.project_document_correlative_uuid == correlative.uuid).all()

                        for log in correlatives_logs:
                            if log.file_uuid:  
                                raise HTTPException(status_code=400, detail=f"Project document correlative {correlative.correlative} has an associated file and cannot be deleted.")
                        
                        correlative.deleted_at = datetime.utcnow()  
                        session.commit()

                    print(f"Soft deleted {len(correlatives_to_delete)} correlatives.")

            if data.ceco is not None:
                project_document_current.ceco = data.ceco

            if data.document_version_uuid is not None:
                project_document_current.document_version_uuid = data.document_version_uuid

            if data.correlative_automatic is not None:
                project_document_current.correlative_automatic = data.correlative_automatic

            if data.correlative is not None:
                project_document_current.correlative = data.correlative

            self.update(db=session, db_obj=project_document_current, obj_in=data)
            session.commit()

            print(f"Project Document {project_document_uuid} updated successfully.")

            return {
                "project_document": {
                    "uuid": project_document_current.uuid,
                    "ceco": project_document_current.ceco,
                    "document_version_uuid": project_document_current.document_version_uuid,
                    "correlative": project_document_current.correlative,
                    "correlative_automatic": project_document_current.correlative_automatic
                }
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    async def delete_project_document(self, project_document_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=project_document_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        
project_document_controller=ProjectDocumentController(ProjectDocument)