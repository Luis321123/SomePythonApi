from sqlalchemy.orm import Session
from app.models.Document import Document as Document_tbl
from app.models.DocumentVersion import DocumentVersion as DocumentVersion_tbl
from app.models.ProjectDocument import ProjectDocument as ProjectDocument_tbl
from app.models.ProjectDocumentCorrelative import ProjectDocumentCorrelative as ProjectDocumentCorrelative_tbl
from sqlalchemy import asc, desc



def get_document_list_controller(
        document_type_uuid: str,
        business_unit_uuid: str,
        management_area_uuid: str,
        ceco: str,
        db: Session,
        discipline_uuid: str = None
    ):
    
    documents = db.query(Document_tbl).filter(
        Document_tbl.document_type_uuid == document_type_uuid
    ).filter(
        Document_tbl.business_unit_uuid == business_unit_uuid
    ).filter(
        Document_tbl.management_area_uuid == management_area_uuid
    ).order_by(
        asc(Document_tbl.discipline_uuid)
    ).order_by(
        asc(Document_tbl.nro)
    )

    if discipline_uuid:
        documents = documents.filter(
            Document_tbl.discipline_uuid == discipline_uuid
        )

    documents = documents.all()
    
    for item in documents:
        code = "-".join(filter(None, [
            item.business_unit.acronym if item.business_unit else "",
            item.management_areas.acronym if item.management_areas else "",
            item.document_type.acronym if item.document_type else "",
            item.disciplines.acronym if item.disciplines else ""
        ]))

        full_code = f"CFLX-{code}" if code else None
        
        item = item.__dict__
        
        item['code'] = full_code + "-" + str(item['nro'])
        
        item['document_version'] = db.query(DocumentVersion_tbl).filter(
            DocumentVersion_tbl.document_uuid == item['uuid']
        ).filter(
            DocumentVersion_tbl.deleted_at == None
        ).order_by(
            desc(DocumentVersion_tbl.created_at)
        ).first()
        
        
        if item['document_version']:
            item['document_version'] = item['document_version'].__dict__
            
            item['document_version']['project_document'] = db.query(ProjectDocument_tbl).filter(
                ProjectDocument_tbl.ceco == ceco
            ).filter(
                ProjectDocument_tbl.deleted_at == None
            ).filter(
                ProjectDocument_tbl.document_version_uuid == item['document_version']['uuid']
            ).order_by(
                desc(ProjectDocument_tbl.created_at)
            ).first()
            
            if item['document_version']['project_document']:
                item['document_version']['project_document'] = item['document_version']['project_document'].__dict__
                item['document_version']['project_document']['project_document_correlative_count'] = db.query(ProjectDocumentCorrelative_tbl).filter(
                    ProjectDocumentCorrelative_tbl.deleted_at == None
                ).filter(
                    ProjectDocumentCorrelative_tbl.project_document_uuid == item['document_version']['project_document']['uuid']
                ).count()
    
    return documents
