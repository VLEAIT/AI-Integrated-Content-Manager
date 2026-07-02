from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserResponse,UserCreate,UserLogin,Token
from database import get_db
from sqlalchemy.orm import Session
from models import User 
from core import hashed_passowrd,verify_password,create_token

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=UserResponse,status_code=201)
def register(user_register:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user_register.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed=hashed_passowrd(user_register.password)
    db_user=User(**user_register.model_dump(exclude={"password","confirm_password"}),hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login",response_model=Token)
def login(user_login:UserLogin,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user_login.email).first()
    if not existing or  not verify_password(user_login.password,existing.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not found")
    token=create_token({"sub":str(existing.id)})
    return {"access_token":token,"token_type":"bearer"}


