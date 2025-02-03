from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.management_areas import ManagementAreasCreate, ManagementAreasUpdate
from app.controllers.management_areas import management_area_controller

router = APIRouter()

@router.get('/management_area',status_code=status.HTTP_200_OK)
async def get_management_area(management_area_uuid: Optional[str]= None, session: Session = Depends(get_session)):
    management_area_current = await management_area_controller.get_management_area(db=session, uuid=management_area_uuid)
    return management_area_current

@router.get('/management_area_filter', status_code=status.HTTP_200_OK)
async def get_multi_management_area(filter_by_name: Optional[str] = None, session: Session = Depends(get_session)):
    activities = await management_area_controller.get_multi_management_area(db=session, filter=filter_by_name)
    return activities

@router.post('/management_area',status_code=status.HTTP_201_CREATED)
async def create_management_area(data:ManagementAreasCreate, session: Session = Depends(get_session)):
    management_current = await management_area_controller.create_management_area(session=session, data=data)
    return management_current

@router.put('/management_area', status_code=status.HTTP_200_OK)
async def update_management_area(uuid: str, data:ManagementAreasUpdate, session: Session = Depends(get_session)):
    await management_area_controller.update_management_area(data=data, management_area_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your management_area has been updated successfully'})

@router.delete('/management_area',status_code=status.HTTP_200_OK)
async def remove_management_area(uuid: str, session: Session = Depends(get_session)):
    await management_area_controller.delete_management_area(management_area_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your management_area has been deleted successfully'})
