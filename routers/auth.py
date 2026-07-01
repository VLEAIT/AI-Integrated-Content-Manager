from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserResponse,UserCreate
from database import get_db
from sqlalchemy.orm import session
from models import User 
from core import hashed_passowrd

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=UserResponse,status_code=201)
def register(user_register:UserCreate,db:session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user_register.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    hashed=hashed_passowrd(user_register.password)
    db_user=User(**user_register.model_dump(exclude={"password","conform_password"}),hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
