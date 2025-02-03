from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.settings import get_settings

settings = get_settings()

def create_application():
    application = FastAPI(
        title="MS Protocolos",
        version="0.0.1",
        description="Bienvenido a MS Protocolos.",
        docs_url="/docs", 
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1, 
            "defaultModelExpandDepth": -1,   
            "docExpansion": "none",
            "persistAuthorization": True,    
            "tryItOutEnabled":True,           
        }
    )

    application.include_router(api_router)
    return application

app = create_application()

origins = [
    str(settings.FRONTEND_HOST)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hi, I am Louis - Your app is done & working, if u have problems contact me (luis1233210e@gmail.com)."}