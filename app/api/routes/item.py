from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.item import get_item, create_item, update_item, delete_item, search_items
from typing import Optional
from schemas.item import ItemCreate, ItemResponse, ItemUpdate, ItemFilter

router = APIRouter(prefix="/items")

@router.post("/", response_model=ItemResponse)
async def create_item_endpoint(
   # nombre: str = Query(..., min_length=3, max_length=50), 
   # origen: Optional[str] =Query(None), 
   # tipo: str  = Query(..., description= "si es piedra o cristal",pattern="^(piedra|cristal)$"), 
   # formato: str = Query(...,description="tienes que elegir entre bruto, rolado o joya", pattern="^(bruto|rolado|joya)$"),
   # composicion:Optional[str] = Query(None),
   # propiedad:Optional[str] = Query(None),
   # precio: Optional[int] = Query(None, ge=0), 
   # venta: Optional[int]=Query(None, ge=0),     
   # proveedor: Optional[str]=Query(None),  
   # imagen_url: Optional[str]=Query(None), 
    item: ItemCreate,
    db: Session = Depends(get_db)):
    
    return create_item(db, item)
    #return create_item(db, nombre, origen, tipo, formato, composicion, propiedad, precio, venta, proveedor, imagen_url)


#@router.get("/search")
#async def get_items(     
#    nombre: Optional[str] = Query( None),
#    origen: Optional[str] = Query(None),
#    tipo: Optional[str] = Query(None),
#    formato:Optional[str] = Query(None),
#    propiedad:Optional[str] = Query(None),
#    precio_min:Optional[int] = Query(None, ge=0),
#    precio_max:Optional[int] = Query(None, ge=0),
#    proveedor:Optional[str] = Query(None),
#    order_by: Optional[str] = Query("nombre", description="campo para ordenar"),
#    order_dir: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
#    skip: int = 0,
#    limit: int = Query(10, ge=1, le=100),
    
#    db: Session = Depends(get_db)):

#    return search_items(
#        db,
#        nombre,
#        origen,
#        tipo,
#        formato,
#        propiedad,
#        precio_min,
#        precio_max,
#        proveedor,
#        order_by,
#        order_dir,
#        skip,
#        limit
#    )

@router.get("/search")
async def get_items(
    filters: ItemFilter = Depends(),
    db: Session = Depends(get_db)
):
    return search_items(db,filters)

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_endpoint(item_id: int, db: Session= Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}")
async def update_item_endpoint(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db)
):
    #item = db.query(Item).filter(Item.id == item_id).first()
    #item = update_item(db, item_id, nombre, origen, tipo, formato, composicion, propiedad, precio, venta, proveedor, imagen_url)
    #if item is None:
    #    raise HTTPException(status_code=404, detail="Item not found")

    #return item

    updated_item = update_item(db, item_id, item)

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


@router.delete("/{item_id}")
async def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = delete_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"detail": "Item deleted"}
