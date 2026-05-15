from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.usuario import Usuario
from schemas.user import UserCreate, UserOut
from core.security import hash_password
from api.deps  import get_current_admin
 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_admin)
):
    # evitar que cualquiera cree admins
    role = "user"
    
    if user_in.role == "admin":
       role = "admin" # solo permitido porque ya es admin quien ejecuta

    new_user = Usuario(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)    

    return new_user
    


