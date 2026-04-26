from sqlalchemy.orm import Session
from models import Item
from typing import List, Optional


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()
    
def create_item(db: Session, nombre: str, origen: str, tipo: str, formato: str, composicion: str,
propiedad: str, precio: int, venta: int, proveedor: str, imagen_url: str):
    db_item = Item(nombre=nombre, origen=origen, tipo=tipo, formato=formato,composicion=composicion,
    propiedad=propiedad, precio=precio, venta=venta, proveedor=proveedor, imagen_url=imagen_url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, nombre: str, origen: str, tipo: str, formato: str, composicion: str,
propiedad: str, precio: int, venta: int, proveedor: str, imagen_url: str):
    item = db.query(Item).filter(Item.id == item_id).first() 
    if item != None:
        item.nombre = nombre
        item.origen = origen
        item.tipo = tipo
        item.formato = formato
        item.composicion = composicion
        item.propiedad = propiedad
        item.precio = precio
        item.venta = venta
        item.proveedor = proveedor
        item.imagen_url = imagen_url
        db.commit()
        db.refresh(item)
         
    return item


def delete_item(db: Session, item_id: int ):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item != None:
        db.delete(item)
        db.commit()

    return item

def search_items( 
    db: Session,
    nombre: Optional[str] = None,
    origen: Optional[str] = None,
    tipo: Optional[str] = None,
    formato:Optional[str] = None,
    propiedad:Optional[str] = None,
    precio_min:Optional[int] = None,
    precio_max:Optional[int] = None,
    proveedor:Optional[str] = None,
    order_by: Optional[str] = None,
    order_dir: Optional[str] = "asc",
    skip: int = 0,
    limit: int = 10) -> List[Item]:

    query = db.query(Item)
    if nombre:
        query = query.filter(Item.nombre.ilike(f"%{nombre}%"))
    
    if origen:
        query = query.filter(Item.origen.ilike(f"%{origen}%"))

    if tipo: 
        query = query.filter(Item.tipo.ilike(f"%{tipo}%"))

    if formato: 
        query = query.filter(Item.formato.ilike(f"%{formato}%"))

    if propiedad: 
        query = query.filter(Item.propiedad.ilike(f"%{propiedad}%"))

    if proveedor: 
        query = query.filter(Item.venta.ilike(f"%{origen}%"))

    if precio_min is not None: 
        query = query.filter(Item.venta >= precio_min)

    if precio_max is not None:
        query = query.filter(Item.venta <= precio_max)

    # ordenamiento dinamico
    if order_by:
        column = getattr(Item, order_by, None)

        if column is not None:
            if order_dir == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    
    return query.offset(skip).limit(limit).all()
