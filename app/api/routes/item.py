from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.item import get_item, create_item, update_item, delete_item, search_items
from typing import Optional
from schemas.item import ItemCreate, ItemResponse, ItemUpdate, ItemFilter
from models.usuario import Usuario
from api.deps import get_current_user, get_current_admin
 
router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemResponse)
async def create_item_endpoint( 
    item: ItemCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)

):
    
    return create_item(db, item)


@router.get("/search")
async def get_items(
    user: Usuario = Depends(get_current_user),
    filters: ItemFilter = Depends(),
    db: Session = Depends(get_db)
):
    return search_items(db,filters)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_endpoint(
    item_id: int, 
    db: Session= Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}")
async def update_item_endpoint(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    updated_item = update_item(db, item_id, item)

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


@router.delete("/{item_id}")
async def delete_item_endpoint(
    item_id: int, 
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    item = delete_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"detail": "Item deleted"}
