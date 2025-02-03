from fastapi import HTTPException

# Constantes para el tamaño de archivo
KB = 1024
MB = 1024 * KB

# Listas de tipos de archivos permitidos
supported_img_filetypes = ['jpeg', 'jpg', 'png', 'bmp']
supported_document_filetypes = ['xlsx', 'pdf', 'docx', 'doc']  # corregido 'doxc'

def validate_file_size(file: bytes):
    """Valida que el tamaño del archivo esté entre 0 y 30 MB"""
    size = len(file)
    if not 0 < size <= 30 * MB:
        raise HTTPException(
            status_code=400,
            detail='Supported file size is 0 - 30 MB'
        )

def suported_file_type(filename: str) -> str:
    """Determina si el archivo es una imagen o un documento según su extensión"""
    # Verificar que el archivo tenga extensión
    if '.' not in filename:
        raise HTTPException(status_code=400, detail="The file has no extension.")
    
    # Obtener la extensión del archivo
    ext = filename.split(".")[-1].lower()
    print(f"File extension: {ext}")  # Agregar depuración para ver qué extensión se está leyendo

    # Comprobar si es una imagen o un documento permitido
    if ext in supported_img_filetypes:
        print(f"File recognized as image.")  # Depuración adicional
        return 'images'
    elif ext in supported_document_filetypes:
        print(f"File recognized as document.")  # Depuración adicional
        return 'documents'
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported types: "
                   f"{', '.join(supported_img_filetypes + supported_document_filetypes)}"
        )
