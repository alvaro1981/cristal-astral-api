from sqlalchemy.orm import Session

from models.usuario import Usuario
from core.security import hash_password


def create_initial_admin(db: Session):

    admin_email = "satan.alarcon@mari.com"
    admin_password = "123456"

    existing_admin = (
        db.query(Usuario)
        .filter(Usuario.role == "admin")
        .first()
    )
    
    if existing_admin:
        print("Ya existe un administrador")
        return

    admin_user = Usuario(
        username="Satansionesco",
        email=admin_email,
        hashed_password=hash_password(admin_password),
        role="admin", 
        is_active=True
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print("Administrador inicial creado")
