from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Form

from app.controllers.autentication import jwtBearer
from app.core.database import get_session
from app.schemas.document_version import DocumentVersionCreate, DocumentVersionUpdate
from app.controllers.document_version import document_version_controller

router = APIRouter()

@router.get('/document_version',status_code=status.HTTP_200_OK)
async def get_document_version(document_version_uuid: Optional[str]= None, document_uuid:str = None, session: Session = Depends(get_session)):
    document_version_current = await document_version_controller.get_document_version(db=session, uuid=document_version_uuid, document_uuid=document_uuid)
    return document_version_current

@router.post('/document_version', status_code=status.HTTP_201_CREATED)
async def create_document_version(document_uuid: str = Form(...),nro: str = Form(...), session: Session = Depends(get_session),file: UploadFile | None = None, user = Depends(jwtBearer(get_user=True))):
    data = DocumentVersionCreate(document_uuid=document_uuid, nro=nro)
    document_versions = await document_version_controller.create_document_version(session=session,data=data,file=file,user_uuid=user['uuid'])
    return document_versions

@router.put('/document_version', status_code=status.HTTP_200_OK)
async def update_document_version(document_version_uuid: str,document_uuid: Optional[str] = Form(None),nro: str = Form(...),session: Session = Depends(get_session),file: UploadFile | None = None, user = Depends(jwtBearer(get_user=True))):
    data = DocumentVersionUpdate(document_uuid=document_uuid, nro=nro)
    document = await document_version_controller.update_document_version(data=data,document_version_uuid=document_version_uuid,session=session,file=file,user_uuid=user['uuid'])
    return document

@router.delete('/document_versions',status_code=status.HTTP_200_OK)
async def delete_document_version(uuid: str, session: Session = Depends(get_session)):
    await document_version_controller.delete_document_version(document_version_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your document_version has been deleted successfully'})