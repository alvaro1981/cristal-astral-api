from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.image_service import upload_item_image

router = APIRouter(prefix="/items", tags=["Item Images"])

@router.post("/{item_id}/upload-image")
def upload_image(
    item_id:int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return upload_item_image(db, item_id, file)
