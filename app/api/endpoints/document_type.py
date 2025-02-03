from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.document_type import DocumentTipeCreate, DocumentTypeUpdate
from app.controllers.document_type import document_type_controller

router = APIRouter()

@router.get('/document_type',status_code=status.HTTP_200_OK)
async def get_document_type(document_type_uuid: Optional[str]= None, session: Session = Depends(get_session)):
    document_type_current = await document_type_controller.get_document_type(db=session, uuid=document_type_uuid)
    return document_type_current

@router.get('/document_type_filter', status_code=status.HTTP_200_OK)
async def get_multi_business_units(filter_by_name: Optional[str] = None, session: Session = Depends(get_session)):
    activities = await document_type_controller.get_multi_document_type(db=session, filter=filter_by_name)
    return activities

@router.post('/document_type',status_code=status.HTTP_201_CREATED)
async def create_document_type(data:DocumentTipeCreate, session: Session = Depends(get_session)):
    document = await document_type_controller.create_document_type(session=session, data=data)
    return document 

@router.put('/document_type', status_code=status.HTTP_200_OK)
async def update_document_type(uuid: str, data:DocumentTypeUpdate, session: Session = Depends(get_session)):
    await document_type_controller.update_document_type(data=data, document_type_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your document_type has been updated successfully'})

@router.delete('/document_type',status_code=status.HTTP_200_OK)
async def remove_document_type(uuid: str, session: Session = Depends(get_session)):
    await document_type_controller.delete_document_type(document_type_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your document_type has been deleted successfully'})
