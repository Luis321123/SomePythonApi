from typing import Optional
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.documents import DocumentsCreate, DocumentsUpdate
from app.controllers.documents import document_controller
from app.controllers.documents_get_controller import get_document_list_controller

router = APIRouter()

@router.get('/documents', status_code=status.HTTP_200_OK)
async def get_document(document_uuid: Optional[str] = None, session: Session = Depends(get_session)):
    document_current = await document_controller.get_documents_with_acronyms(db=session, uuid=document_uuid)
    return document_current

@router.get('/documents_list', status_code=status.HTTP_200_OK)
async def get_document_list(document_type_uuid:str,business_unit_uuid:str,management_area_uuid:str,ceco_of_project:str,discipline_uuid:str = None,db: Session = Depends(get_session)):
    return get_document_list_controller(document_type_uuid=document_type_uuid, business_unit_uuid=business_unit_uuid, management_area_uuid=management_area_uuid, discipline_uuid=discipline_uuid, db=db, ceco=ceco_of_project)

@router.get('/documents_filter', status_code=status.HTTP_200_OK)
async def get_multi_business_units(business_unit_uuid: Optional[str] = None, session: Session = Depends(get_session)):
    activities = await document_controller.get_multi_document(db=session, business_unit_uuid=business_unit_uuid)
    return activities

@router.get('/search_document', status_code=status.HTTP_200_OK)
async def search_project_document(business_unit_uuid: Optional[str] = None,management_area_uuid: Optional[str] = None,name: Optional[str] = None, nro: Optional[int] = None, document_type_uuid: Optional[str] = None, discipline_uuid: Optional[str] = None, session: Session = Depends(get_session)):
    results = await document_controller.search_document(db=session,business_unit_uuid=business_unit_uuid,management_area_uuid=management_area_uuid,document_type_uuid=document_type_uuid,discipline_uuid=discipline_uuid, name= name, nro = nro)
    return results

@router.post('/documents',status_code=status.HTTP_201_CREATED)
async def create_document(data:DocumentsCreate = Form(...), session: Session = Depends(get_session)):
    documents = await document_controller.create_document(session=session, data=data)
    return documents

@router.put('/documents', status_code=status.HTTP_200_OK)
async def update_document(uuid: str, data:DocumentsUpdate = Form(...), session: Session = Depends(get_session)):
    document_put = await document_controller.update_document(data=data, document_uuid=uuid, session=session)
    return document_put

@router.delete('/documents',status_code=status.HTTP_200_OK)
async def delete_document_version(uuid: str, session: Session = Depends(get_session)):
    await document_controller.delete_document(document_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your document has been deleted successfully'})