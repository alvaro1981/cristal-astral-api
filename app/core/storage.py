import os 
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import UPLOAD_DIR, STATIC_URL, ALLOWED_IMAGE_TYPES
from fastapi import HTTPException 

os.makedirs(UPLOAD_DIR, exist_ok=True)

class LocalStorage:
    def save(self, file: UploadFile) -> str:
        # validat tipo MIME
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException( status_code=400, detail="Formato de iamgen no permitido")

        # generar nombre unico
                 
        extension = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{extension}"
       
        file_path =  UPLOAD_DIR / filename	 
        #guardar archivo
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        # URL accesible ( luego se puede cambiar eso a S3 sin romper nada)
        #return f"/uploads/{filename}"
        return f"{STATIC_URL}/{filename}"
