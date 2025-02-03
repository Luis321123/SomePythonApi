from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4

from app.utils.files import validate_file_size, suported_file_type
from app.schemas.file import FileCreate, FileUpdate
from app.services.base import CRUDBase
from app.models.File import File_tb
from app.services.s3 import AWS_S3_ZONE, s3_upload
from app.core.settings import get_settings

settings = get_settings()

AWS_S3_BUCKET = settings.AWS_S3_BUCKET


class fake_file():
    filename:str
    size:int
    content_type:str = 'application/pdf'

    def __init__(self, filename:str, content:bytes):
        self.filename = filename
        self.size = content.__len__()

class FileController(CRUDBase[File_tb, FileCreate, FileUpdate]):
    async def get_file(self, db:Session, uuid: str):
        if uuid:
            files = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.deleted_at == None).first()
            if not files:
                raise HTTPException(status_code=404, detail="uuid of document_project not found.")
            return files
        else:
            return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()).all()
   
    async def update_file(self, data: FileUpdate, File_uuid: str, session: Session):
        try:
            file_current = await self.get_file(db=session, uuid=File_uuid)
            
            self.update(db=session, db_obj=file_current, obj_in=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
        

    async def delete_file(self, File_uuid:str, session: Session):
        try:
            self.remove(db=session, uuid=File_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    

    async def upload_file(self, file: File_tb, comment: str, db: Session, user_uuid: str, supported_file: str = None) -> File_tb | str:
        """supported_file_type accepts 'images' and 'documents'"""
        try:
            # Leer el contenido del archivo
            content = await file.read()
        except Exception as error:
            raise HTTPException(status_code=400, detail=f"Error reading file: {error}")
        
        # Validaar tamaño del archivo
        validate_file_size(content)

        # Determinar el tipo de archivo (imagen o documento)
        folder = suported_file_type(file.filename)  # Asegúrate de que esta función esté manejando correctamente las imágenes y documentos
        print(f"File type determined: {folder}")  # Agregar una verificación de depuración

        # Verificar si el tipo de archivo permitido coincide con lo esperado
        if supported_file and folder != supported_file:
            raise HTTPException(status_code=400, detail=f"Unsupported file type, expected a {supported_file.replace('s', '')}.")
        
        # Crear la entrada del archivo en la base de datos
        query = File_tb()
        query.comment = comment
        query.ext = file.filename.split('.')[-1].lower()  # Obtener la extensión del archivo
        query.name = f'{uuid4()}.{query.ext}'  # Crear un nombre único para el archivo
        query.folder = folder
        query.path = f'https://s3.{AWS_S3_ZONE}.amazonaws.com/{AWS_S3_BUCKET}/{folder}/{query.name}'  # Definir la ruta de S3
        query.size = len(content)  # Usar el tamaño del contenido leído
        query.created_by = user_uuid

        # Subir el archivo a S3
        try:
            await s3_upload(contents=content, key=f"{folder}/{query.name}", Content_Type=file.content_type)
        except Exception as s3_error:
            raise HTTPException(status_code=500, detail=f"Error uploading to S3: {s3_error}")
        
        # Guardar en la base de datos
        db.add(query)
        db.commit()
        db.refresh(query)

        return query

    
file_controller=FileController(File_tb)