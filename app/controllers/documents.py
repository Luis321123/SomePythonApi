from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException

from sqlalchemy.orm import aliased
from app.models import DocumentVersion, ProjectDocument
from app.models.ProjectDocumentCorrelative import ProjectDocumentCorrelative
from app.schemas.documents import DocumentsCreate, DocumentsUpdate
from app.services.base import CRUDBase
from app.models.Document import Document

class DocumentController(CRUDBase[Document, DocumentsCreate, DocumentsUpdate]):

    async def get_documents_with_acronyms(self, db: Session, uuid: str = None, include_deleted: bool = False):
        DocumentType = aliased(self.model.document_type.property.entity)
        BusinessUnit = aliased(self.model.business_unit.property.entity)
        ManagementArea = aliased(self.model.management_areas.property.entity)
        Discipline = aliased(self.model.disciplines.property.entity)
        DocumentVersion = aliased(self.model.document_versions.property.entity)

        if uuid:
            query = db.query(self.model).outerjoin(DocumentType, self.model.document_type_uuid == DocumentType.uuid)\
                .outerjoin(BusinessUnit, self.model.business_unit_uuid == BusinessUnit.uuid)\
                .outerjoin(ManagementArea, self.model.management_area_uuid == ManagementArea.uuid)\
                .outerjoin(Discipline, self.model.discipline_uuid == Discipline.uuid)\
                .filter(self.model.uuid == uuid)

            if not include_deleted:
                query = query.filter(self.model.deleted_at == None)

            document = query.first()

            if not document:
                raise HTTPException(status_code=404, detail="UUID of the document not found.")

            latest_version = db.query(DocumentVersion).filter(
                DocumentVersion.document_uuid == document.uuid,
                DocumentVersion.deleted_at == None
            ).order_by(desc(DocumentVersion.created_at)).first()

            code = "-".join(filter(None, [
                document.business_unit.acronym if document.business_unit else "",
                document.management_areas.acronym if document.management_areas else "",
                document.document_type.acronym if document.document_type else "",
                document.disciplines.acronym if document.disciplines else ""
            ]))

            return {
                "code": "CFLX-" + code + "-" + str(document.nro),
                "uuid": document.uuid,
                "name": document.name,
                "nro": document.nro,
                "discipline_uuid": document.discipline_uuid,
                "document_type_uuid": document.document_type_uuid,
                "business_unit_uuid": document.business_unit_uuid,
                "management_area_uuid": document.management_area_uuid,
                "document_version": latest_version.uuid if latest_version else None,
                "document_version_nro": latest_version.nro if latest_version else None,
                "last_file": latest_version.file.path if latest_version and latest_version.file and latest_version.file.path else None,
                "created_at": document.created_at,
                "deleted_at": document.deleted_at
            }

        query = db.query(self.model).outerjoin(DocumentType, self.model.document_type_uuid == DocumentType.uuid)\
            .outerjoin(BusinessUnit, self.model.business_unit_uuid == BusinessUnit.uuid)\
            .outerjoin(ManagementArea, self.model.management_area_uuid == ManagementArea.uuid)\
            .outerjoin(Discipline, self.model.discipline_uuid == Discipline.uuid)

        if not include_deleted:
            query = query.filter(self.model.deleted_at == None)

        documents = query.all()

        result = []
        for document in documents:
            latest_version = db.query(DocumentVersion).filter(
                DocumentVersion.document_uuid == document.uuid,
                DocumentVersion.deleted_at == None
            ).order_by(desc(DocumentVersion.created_at)).first()

            code = "-".join(filter(None, [
                document.business_unit.acronym if document.business_unit else "",
                document.management_areas.acronym if document.management_areas else "",
                document.document_type.acronym if document.document_type else "",
                document.disciplines.acronym if document.disciplines else ""
               ]))

            result.append({
                "code": "CFLX-" + code + "-" + str(document.nro),
                "uuid": document.uuid,
                "name": document.name,
                "nro": document.nro,
                "discipline_uuid": document.discipline_uuid,
                "document_type_uuid": document.document_type_uuid,
                "business_unit_uuid": document.business_unit_uuid,
                "management_area_uuid": document.management_area_uuid,
                "document_version": latest_version.uuid if latest_version else None,
                "document_version_nro": latest_version.nro if latest_version else None,
                "last_file": latest_version.file.path if latest_version and latest_version.file and latest_version.file.path else None,
                "created_at": document.created_at,
                "deleted_at": document.deleted_at,
            })

        return result
    
    async def get_multi_document(self, db: Session, business_unit_uuid: str = None):
        try:
            base_query = db.query(self.model).where(self.model.deleted_at == None).order_by(self.model.created_at.desc())

            if business_unit_uuid and business_unit_uuid != "null":
                base_query = base_query.filter(self.model.business_unit_uuid == business_unit_uuid)

            return base_query.all()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")
        
    async def get_document_by_uuid(self, uuid: str, session: Session):
        try:
            document = session.query(self.model).filter(self.model.uuid == uuid).first()
            
            if not document:
                return None
            
            return document
 
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")

    async def create_document(self, data: DocumentsCreate, session: Session):
        try:
            new_document = self.create(db=session, obj_in=data)
            return new_document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

    async def search_document(self, db: Session, *, business_unit_uuid: str = None,management_area_uuid: str = None, document_type_uuid: str = None,discipline_uuid: str = None,nro: int = None,correlative: int = None,name: str = None):
        try:
            query = db.query(self.model).filter(self.model.deleted_at == None)

            if business_unit_uuid:
                query = query.filter(self.model.business_unit_uuid == business_unit_uuid)
            if management_area_uuid:
                query = query.filter(self.model.management_area_uuid == management_area_uuid)
            if name:
                query = query.filter(self.model.name.ilike(f"%{name}%"))
            if document_type_uuid:
                query = query.filter(self.model.document_type_uuid == document_type_uuid)
            if discipline_uuid:
                query = query.filter(self.model.discipline_uuid == discipline_uuid)
            if correlative is not None:
                query = query.filter(self.model.correlative == correlative)
            if nro:
                query = query.filter(self.model.nro == nro)

            results = query.all()

            if not results:
                raise HTTPException(status_code=404, detail="No project documents found.")
            
            return results
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Hay un error:{str(e)}")
    
    async def update_document(self, data: DocumentsUpdate, document_uuid: str, session: Session):
        try:
            document_current = await self.get_document_by_uuid(session=session, uuid=document_uuid)
       
            
            if isinstance(document_current, dict):  # Si por alguna razón es un diccionario
                raise HTTPException(status_code=400, detail="Se esperaba un objeto, pero se recibió un diccionario.")
            
            document = self.update(db=session, db_obj=document_current, obj_in=data)
            return document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating document: {str(e)}")

        
    async def delete_document(self, document_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=document_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        
    async def get_document_list(self, uuid: str, session: Session):
        try:
            document = session.query(self.model).filter(self.model.uuid == uuid).first()

            if not document:
                raise HTTPException(status_code=404, detail="Document not found.")

            document_versions = session.query(DocumentVersion).filter(DocumentVersion.document_uuid == document.uuid).all()

            # Listas separaadas para project_documents y correlatives
            project_document_uuids = []
            correlatives = []

            for version in document_versions:
                project_documents = session.query(ProjectDocument).filter(
                    ProjectDocument.document_version_uuid == version.uuid
                ).all()

                if project_documents:
                    # Añadir solo el uuid de los ProjectDocuments aa la lista
                    for project_doc in project_documents:
                        project_document_uuids.append(project_doc.uuid)

                        # Agregar correlativo solo si no es None o si es un número válido
                        if project_doc.correlative is not None:
                            correlatives.append(project_doc.correlative)


                else:
                    correlatives.append(None)

            document_versions = session.query(DocumentVersion).filter(DocumentVersion.document_uuid == document.uuid, DocumentVersion.deleted_at == None).all()
            correlatives = [correlative for correlative in correlatives if correlative is not None]
            document_version_uuids = [version.uuid for version in document_versions]
            document_version_nro = [version.nro for version in document_versions]

            code = "-".join(filter(None, [
                document.business_unit.acronym if document.business_unit else "",
                document.management_areas.acronym if document.management_areas else "",
                document.disciplines.acronym if document.disciplines else "",
                document.document_type.acronym if document.document_type else ""
            ]))

            return {
                "code": "CFLX-" + code + "-" + str(document.nro),
                "uuid": document.uuid,
                "name": document.name,
                "nro": document.nro,
                "discipline_uuid": document.discipline_uuid,
                "document_type_uuid": document.document_type_uuid,
                "business_unit_uuid": document.business_unit_uuid,
                "management_area_uuid": document.management_area_uuid,
                "document_versions": document_version_uuids,
                "document_version_nro": document_version_nro,
                "project_documents": project_document_uuids,  # Solo UUIDs de ProjectDocuments
                "correlatives": correlatives,  # Solo números de correlativos
                "created_at": document.created_at,
                "deleted_at": document.deleted_at
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving documents : {str(e)}")




document_controller=DocumentController(Document)

