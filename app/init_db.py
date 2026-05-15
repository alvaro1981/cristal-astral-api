from database import engine, Base, SessionLocal
from models import Item, Usuario
from bootstrap_admin_user import create_initial_admin

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        create_initial_admin(db) 
   
    finally:
        db.close()
   
