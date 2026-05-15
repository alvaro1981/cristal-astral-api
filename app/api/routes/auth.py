from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm


from database import get_db
from services.auth_service import authenticate_user
from core.security import create_access_token
from schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectas",
        )
    
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
