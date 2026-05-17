from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import verify_password


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(Usuario).filter(
        Usuario.email == email
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
