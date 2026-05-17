from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email=Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(255), index=True)
    role = Column(String(255), default ="user",  index=True)
    is_active = Column(Boolean, default=True)
