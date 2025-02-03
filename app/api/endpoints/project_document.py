from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.projects_documents import ProjectDocumentCreate, ProjectDocumentUpdate
from app.controllers.project_document import project_document_controller

router = APIRouter()

@router.get('/project_document',status_code=status.HTTP_200_OK)
async def get_project_documents(project_document_uuid: Optional[str]= None, session: Session = Depends(get_session)):
    document_version_current = await project_document_controller.get_project_document(db=session, uuid=project_document_uuid)
    return document_version_current
@router.get('/search_project_document', status_code=status.HTTP_200_OK)
async def search_project_document(ceco: Optional[str] = None,document_version_uuid: Optional[str] = None,session: Session = Depends(get_session)):
    results = await project_document_controller.search_project_document(db=session,ceco=ceco,document_version_uuid=document_version_uuid)
    return results

@router.post('/project_document', status_code=status.HTTP_201_CREATED)
async def create_project_document(data: ProjectDocumentCreate = Form(...), session: Session = Depends(get_session)):
    project_documents = await project_document_controller.create_project_document(session=session, data=data)
    return {
        "project_document": project_documents['project_document'],
        "correlatives": project_documents['correlatives']
    }
@router.put('/project_document', status_code=status.HTTP_200_OK)
async def update_project_document(project_document_uuid: str,data: ProjectDocumentUpdate = Form(...),session: Session = Depends(get_session)):
        response = await project_document_controller.update_project_document(data=data, project_document_uuid=project_document_uuid, session=session)
        return response

@router.delete('/project_document',status_code=status.HTTP_200_OK)
async def remove_management_area(uuid: str, session: Session = Depends(get_session)):
    await project_document_controller.delete_project_document(project_document_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your project_document has been deleted successfully'})
