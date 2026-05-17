from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.item import Item
from app.core.storage import LocalStorage

storage = LocalStorage()

def upload_item_image(db:Session, item_id: int, file: UploadFile):
    
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="item no encontrado")

    image_url = storage.save(file)

    item.imagen_url = image_url
    db.commit()
    db.refresh(item)

    return item

