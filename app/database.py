from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

# MySQL credentials with host Ubuntu (linux)
# DATABASE_URL = "mysql+pymysql://root:alvaro1981@localhost:3306/cristal_database"

# Credenciales MySql para contenedor con docker 
DATABASE_URL = "mysql+pymysql://root:alvaro1981@mysql_db:3306/cristal_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

# Dependence to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
