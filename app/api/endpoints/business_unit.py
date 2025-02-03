from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.business_unit import BusinessUnitCreate, BusinessUnitUpdate
from app.controllers.business_unit import Business_unit as business_unit_controller

router = APIRouter()

@router.get('/business',status_code=status.HTTP_200_OK)
async def get_business_unit(business_unit_uuid: Optional[str]= None, session: Session = Depends(get_session)):
    business_unit_current = await business_unit_controller.get_business_unit(db=session, uuid=business_unit_uuid)
    return business_unit_current

@router.post('/business',status_code=status.HTTP_201_CREATED)
async def create_business_unit(data:BusinessUnitCreate, session: Session = Depends(get_session)):
    business = await business_unit_controller.create_business_unit(session=session, data=data)
    return business

@router.put('/business', status_code=status.HTTP_200_OK)
async def update_business_unit(uuid: str, data:BusinessUnitUpdate, session: Session = Depends(get_session)):
    await business_unit_controller.update_business_unit(data=data, business_unit_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your business unit has been updated successfully'})

@router.delete('/business',status_code=status.HTTP_200_OK)
async def delete_business_unit(uuid: str, session: Session = Depends(get_session)):
    await business_unit_controller.delete_business_unit(business_unit_uuid=uuid, session=session)
    return JSONResponse({'message': 'Your business unit has been deleted successfully'})