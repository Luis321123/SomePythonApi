from typing import Optional
from fastapi import APIRouter, Depends, Form, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.controllers.autentication import jwtBearer
from app.core.database import get_session
from app.schemas.project_document_correlative import ProjectDocumentCorrelativeCreate, ProjectDocumentCorrelativeUpdate
from app.controllers.project_document_correlative import project_document_correlative_controller

router = APIRouter()

@router.get('/project_document_correlative', status_code=status.HTTP_200_OK)
async def get_project_document(project_document_correlative_uuid: Optional[str] = None,include_deleted: bool = False,  session: Session = Depends(get_session)):
    return await project_document_correlative_controller.get_project_document_correlative(db=session,uuid=project_document_correlative_uuid,include_deleted=include_deleted)

# UUID - project_document_uuid

@router.get('/project_document_filter', status_code=status.HTTP_200_OK)
async def get_multi_project_document_correlative(project_document_uuid: Optional[str] = None, session: Session = Depends(get_session)):
    activities = await project_document_correlative_controller.get_multi_project_document_correlative(db=session, project_document_uuid=project_document_uuid)
    return activities

@router.post('/project_document_correlative', status_code=status.HTTP_201_CREATED)
async def create_project_documents_correlatives(project_document_uuid: str = Form(...),correlative: Optional[str] = Form(None), session: Session = Depends(get_session)):
    correlative_int = int(correlative) if correlative is not None else None
    data = ProjectDocumentCorrelativeCreate(project_document_uuid=project_document_uuid,correlative=correlative_int)
    document_correlative = await project_document_correlative_controller.create_projec_document_correlative(session=session,data=data)
    return document_correlative
  
@router.put('/project_document_correlative', status_code=status.HTTP_200_OK)
async def update_project_document_correlative(document_correlative_uuid: str, correlative: Optional[int] = Form(None),upload_by: Optional[str] = Form(None), file: UploadFile | None = None,session: Session = Depends(get_session),user = Depends(jwtBearer(get_user=True))):
    if file:
        print(f"File received: {file.filename}")
    else:
        print("No file received.")
    data = ProjectDocumentCorrelativeUpdate(correlative=correlative)
    document_correlative = await project_document_correlative_controller.update_projec_document_correlative(data=data,document_correlative_uuid=document_correlative_uuid,session=session,upload_by=upload_by,file=file, user_uuid=user['uuid'])
    return document_correlative

@router.delete('/project_document_correlative',status_code=status.HTTP_200_OK)
async def remove_projknt_document_correlative(project_document_correlative_uuid: str, session: Session = Depends(get_session)):
    await project_document_correlative_controller.delete_project_document_correlative(project_document_correlative_uuid=project_document_correlative_uuid, session=session)
    return JSONResponse({'message': 'Your document_correlative has been deleted successfully'})
