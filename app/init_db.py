from database import engine, Base
from models import Item, Usuario

def init_db():
    Base.metadata.create_all(bind=engine)
