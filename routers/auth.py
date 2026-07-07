from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserResponse,UserCreate,UserLogin,Token,UserUpdate,UserPasswordUpdate
from database import get_db
from sqlalchemy.orm import Session
from models import User 
from core import hashed_passowrd,verify_password,create_token,get_current_user
from typing import Annotated

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
)


DatabaseSession =Annotated[Session,Depends(get_db)]
CurrentUser=Annotated[User,Depends(get_current_user)]

@router.post("/register", response_model=UserResponse,status_code=201)
def register(user_register:UserCreate,db:DatabaseSession):
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
def login(user_login:UserLogin,db:DatabaseSession):
    existing=db.query(User).filter(User.email==user_login.email).first()
    if not existing or  not verify_password(user_login.password,existing.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not found")
    token=create_token({"sub":str(existing.id)})
    return {"access_token":token,"token_type":"bearer"}


@router.patch("/update",response_model=UserResponse)
def update(user_update:UserUpdate,db:DatabaseSession,current_user:CurrentUser):
    update_data=user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="field not filed")
    
    if "user_name" in update_data:
        existing =db.query(User).filter(User.user_name==update_data["user_name"]).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User name already taken")
        

    for key,value in  update_data.items():
        setattr(current_user,key,value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("/password_change")
def update_password(user_update:UserPasswordUpdate,db:DatabaseSession,current_user:CurrentUser):
    if current_user.hashed_password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="logged via the othrer third party source like google")
    if not verify_password(user_update.old_password,current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect password")
    if user_update.old_password == user_update.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="new and old password cannot be same")
    current_user.hashed_password=hashed_passowrd(user_update.new_password)

    db.add(current_user)
    db.commit()
    return{"status":"sucess","detail":"Password updated succesfully"}

    
    