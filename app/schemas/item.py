from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    nombre: str
    origen: Optional[str] = None 
    tipo: str 
    formato: str
    composicion:Optional[str] = None
    propiedad:Optional[str] = None
    precio: Optional[int] = None 
    venta: Optional[int] = None     
    proveedor: Optional[str] = None  
    imagen_url: Optional[str] = None 
    
class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemUpdate(BaseModel):
    nombre: Optional[str] = None
    origen: Optional[str] = None
    tipo: Optional[str] = None
    formato: Optional[str] = None
    composicion: Optional[str] = None
    propiedad: Optional[str] = None
    precio: Optional[int] = None
    venta: Optional[int] = None
    proveedor: Optional[str] = None
    imagen_url: Optional[str] = None


class ItemFilter(BaseModel):
    nombre: Optional[str] = None
    origen: Optional[str] = None
    tipo: Optional[str] = None
    formato: Optional[str] = None
    propiedad: Optional[str] = None
    proveedor: Optional[str] = None

    precio_min: Optional[int] = Field(None, ge=0)
    precio_max: Optional[int] = Field(None, ge=0)

    order_by: Optional[str] = "nombre"
    order_dir: Optional[str] = Field("asc", pattern="^(asc|desc)$")

    skip: int = 0
    limit: int = Field(10, ge=1, le=100)
