from fastapi import APIRouter, Depends


from app.api.endpoints.business_unit import router as router_business_unit
from app.api.endpoints.disciplines import router as router_disciplines
from app.api.endpoints.document_type import router as router_document_type
from app.api.endpoints.document_version import router as router_document_version
from app.api.endpoints.documents import router as router_document
from app.api.endpoints.debug import router as router_debug
from app.api.endpoints.health_check import router as router_check
from app.api.endpoints.management_areas import router as router_management_area
from app.api.endpoints.project_document import router as router_project_document
from app.api.endpoints.project_document_correlative import router as router_project_document_correlative
from app.api.endpoints.project_document_correlative_log import router as router_project_document_correlative_log
from app.api.endpoints.file import router as router_files
from app.controllers.autentication import jwtBearer

api_router = APIRouter()

#route Checkout
api_router.include_router(router_check, tags=["HealthCheck"],
    responses={404: {"description": "Not found"}})
 
#router business

api_router.include_router(router_business_unit, tags=["Business_unit"],
   responses={404: {"description": "Not found"}},
   dependencies=[Depends(jwtBearer())])


#router document_type
api_router.include_router(router_document_type, tags=["Document_type"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])
#routes disciplines
api_router.include_router(router_disciplines, tags=["Discipline"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])


#routes document_version
api_router.include_router(router_document_version, tags=["Document_version"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes document
api_router.include_router(router_document, tags=["Document"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes management_area
api_router.include_router(router_management_area, tags=["management_area"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes document_correlative
api_router.include_router(router_project_document_correlative, tags=["project_document_correlative"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes project_document_correlative_log
api_router.include_router(router_project_document_correlative_log, tags=["project_document_correlative_log"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes project_document
api_router.include_router(router_project_document, tags=["project_document"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])

#routes files
api_router.include_router(router_files, tags=["files"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwtBearer())])


 #routes debug
api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}})


