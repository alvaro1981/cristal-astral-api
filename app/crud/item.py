from sqlalchemy.orm import Session
from models import Item
from typing import List, Optional
from schemas.item import ItemCreate, ItemUpdate, ItemFilter

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()
    
#def create_item(db: Session, nombre: str, origen: str, tipo: str, formato: str, composicion: str,
#propiedad: str, precio: int, venta: int, proveedor: str, imagen_url: str):
#    db_item = Item(nombre=nombre, origen=origen, tipo=tipo, formato=formato,composicion=composicion,
#    propiedad=propiedad, precio=precio, venta=venta, proveedor=proveedor, imagen_url=imagen_url)
def create_item(db: Session,  item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_data: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if not db_item:
        return None

    for key, value in item_data.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


#def update_item(db: Session, item_id: int, nombre: str, origen: str, tipo: str, formato: str, composicion: str,
#propiedad: str, precio: int, venta: int, proveedor: str, imagen_url: str):
#    item = db.query(Item).filter(Item.id == item_id).first() 
#    if item != None:
#        item.nombre = nombre
#        item.origen = origen
#        item.tipo = tipo
#        item.formato = formato
#        item.composicion = composicion
#        item.propiedad = propiedad
#        item.precio = precio
#        item.venta = venta
#        item.proveedor = proveedor
#        item.imagen_url = imagen_url
#        db.commit()
#        db.refresh(item)
         
#    return item


def delete_item(db: Session, item_id: int ):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item != None:
        db.delete(item)
        db.commit()

    return item

def search_items(db: Session, filters: ItemFilter):
    query = db.query(Item)
    if filters.nombre:
        query = query.filter(Item.nombre.ilike(f"%{filters.nombre}%"))
    
    if filters.origen:
        query = query.filter(Item.origen.ilike(f"%{filters.origen}%"))

    if filters.tipo: 
        query = query.filter(Item.tipo.ilike(f"%{filters.tipo}%"))

    if filters.formato: 
        query = query.filter(Item.formato.ilike(f"%{filters.formato}%"))

    if filters.propiedad: 
        query = query.filter(Item.propiedad.ilike(f"%{filters.propiedad}%"))

    if filters.proveedor: 
        query = query.filter(Item.proveedor.ilike(f"%{filters.proveedor}%"))

    if filters.precio_min is not None: 
        query = query.filter(Item.venta >= filters.precio_min)

    if filters.precio_max is not None:
        query = query.filter(Item.venta <= filters.precio_max)

    # ordenamiento dinamico
    if filters.order_by:
        column = getattr(Item, filters.order_by, None)

        if column is not None:
            if filters.order_dir == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    
    return query.offset(filters.skip).limit(filters.limit).all()
