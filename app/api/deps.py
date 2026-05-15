from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer

from core.security import SECRET_KEY, ALGORITHM
from schemas.auth import TokenData
from database import get_db
from models.usuario import Usuario 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user( 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)           

    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.email == token_data.email).first()

    if user is None:
        raise credentials_exception
    
    return user

def get_current_admin(current_user:Usuario = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de administrador"
        )
    return current_user
