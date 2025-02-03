from typing import Optional
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.disciplines import DisciplinesCreate, DisciplinesUpdate
from app.controllers.disciplines import discipline_controller

router = APIRouter()

@router.get('/disciplines')
async def get_disciplines(discipline_uuid: Optional[str] = None,session: Session = Depends(get_session)):
    disciplines = await discipline_controller.get_discipline(db=session,uuid=discipline_uuid)
    return disciplines

@router.get('/disciplines_filter', status_code=status.HTTP_200_OK)
async def get_multi_business_units(filter_by_name: Optional[str] = None,business_unit_uuid: Optional[str] = None,session: Session = Depends(get_session)):
    activities = await discipline_controller.get_multi_disciplines(db=session, filter=filter_by_name, business_unit_uuid=business_unit_uuid)
    return activities

@router.post('/disciplines', status_code=status.HTTP_201_CREATED)
async def create_discipline(data: DisciplinesCreate = list[str], session: Session = Depends(get_session)):
    discipline = await discipline_controller.create_discipline(data=data, session=session)
    return discipline

@router.put('/disciplines', status_code=status.HTTP_200_OK)
async def update_discipline(discipline_uuid: str, data:DisciplinesUpdate=str, session: Session = Depends(get_session)):
    update = await discipline_controller.update_discipline(data=data, disciplines_uuid=discipline_uuid, session=session)
    return update

@router.delete('/disciplines',status_code=status.HTTP_200_OK)
async def delete_discipline(uuid: str, session: Session = Depends(get_session)):
    await discipline_controller.delete_discipline(disciplines_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your Discipline has been deleted successfully'})