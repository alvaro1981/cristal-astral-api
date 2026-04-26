from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"
    id  = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    origen = Column(String(255), index=True)
    tipo = Column(String(255), nullable=False, index=True)
    formato = Column(String(255), nullable=False, index=True)
    composicion = Column(String(255), index=True)
    propiedad = Column(String(255), index=True)
    precio = Column(Integer)
    venta  = Column(Integer)
    proveedor = Column(String(255), index=True)
    imagen_url = Column(String(255))

    

