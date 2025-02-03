from typing import Optional
from fastapi import APIRouter, Depends, Form,  status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException

from app.controllers.autentication import jwtBearer
from app.core.database import get_session
from app.schemas.file import  FileUpdate
from app.controllers.files import file_controller

router = APIRouter()

@router.get('/file',status_code=status.HTTP_200_OK)
async def get_files(file_uuid:Optional[str]= None, session: Session = Depends(get_session)):
    file_current = await file_controller.get_file(db=session, uuid=file_uuid)
    return file_current

@router.post('/upload_file', status_code=200)
async def upload_file(file: UploadFile = File(...), comment: str = Form(...),    session: Session = Depends(get_session),  user = Depends(jwtBearer(get_user=True))):
    try:
        uploaded_file_path = await file_controller.upload_file(file=file,comment=comment,db=session,user_uuid=user['uuid'],supported_file='images' if file.content_type.startswith('image/') else 'documents')
        return {"file_path": uploaded_file_path}
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")

@router.put('/file', status_code=status.HTTP_200_OK)
async def update_files(file_uuid: str, data:FileUpdate, session: Session = Depends(get_session)):
    await file_controller.update_file(data=data, file_uuid=file_uuid, session=session)
    return JSONResponse({'message': 'Your File has been updated successfully'})

@router.delete('/file',status_code=status.HTTP_200_OK)
async def delete_files(uuid: str, session: Session = Depends(get_session)):
    await file_controller.delete_file(file_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your File has been deleted successfully'})
