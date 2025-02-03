from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.controllers.autentication import jwtBearer
from app.core.database import get_session
from app.schemas.project_document_correlative_logs import ProjectDocumentCorrelativeLogCreate, ProjectDocumentCorrelativeLogUpdate, ProjectDocumentCorrelativeLogWithRelations
from app.controllers.project_document_correlative_logs import project_document_correlative_log_controller

router = APIRouter()

@router.get('/project_document_correlative_logs', status_code=status.HTTP_200_OK, response_model=List[ProjectDocumentCorrelativeLogWithRelations])
async def get_project_document_correlative_logs(project_document_correlative_uuid: Optional[str] = None,include_deleted: bool = False,session: Session = Depends(get_session)):
    return await project_document_correlative_log_controller.get_project_document_correlative_logs(db=session,project_document_correlative_uuid=project_document_correlative_uuid,include_deleted=include_deleted)
# UUID - project_document_uuid

@router.get('/project_document_filter_log', status_code=status.HTTP_200_OK, response_model=List[ProjectDocumentCorrelativeLogWithRelations])
async def get_multi_project_document_correlative(project_document_uuid_log: Optional[str] = None, session: Session = Depends(get_session)):
    activities = await project_document_correlative_log_controller.get_multi_project_document_correlative_logs(db=session, project_document_uuid=project_document_uuid_log)
    return activities

@router.post('/project_document_correlative_log', status_code=status.HTTP_201_CREATED)
async def create_project_documents_correlatives(project_document_correlative_uuid: str = Form(...),file: UploadFile | None = None,session: Session = Depends(get_session),user: dict = Depends(jwtBearer(get_user=True))):
    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    if not user_name:
        raise HTTPException(status_code=400, detail="User name not found in token")
    data = ProjectDocumentCorrelativeLogCreate(project_document_correlative_uuid=project_document_correlative_uuid,user_name=user_name  )
    document_correlative = await project_document_correlative_log_controller.create_projec_document_correlative_logs(session=session,data=data,file=file,user_name=user_name)
    return document_correlative

@router.put('/project_document_correlative_log', status_code=status.HTTP_200_OK)
async def update_project_document_correlative_log(project_document_correlative_log_uuid: str,status: Optional[bool] = None,status_comment: Optional[str] = None,session: Session = Depends(get_session),user: dict = Depends(jwtBearer(get_user=True))):
    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    if not user_name:
        raise HTTPException(status_code=400, detail="User name not found in token")
    
    document_correlative = await project_document_correlative_log_controller.update_project_document_correlative_status(status_comment=status_comment,document_correlative_uuid=project_document_correlative_log_uuid,status=status,session=session,user_name=user_name)

    return document_correlative

@router.delete('/project_document_correlative_log', status_code=status.HTTP_200_OK)
async def remove_project_document_correlative_logs(project_document_correlative_log_uuid: str, session: Session = Depends(get_session)):
    await project_document_correlative_log_controller.delete_project_document_correlative_logs(project_document_correlative_log_uuid, session=session)
    return JSONResponse({'message': 'Your document_correlative has been deleted successfully'})