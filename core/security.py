from passlib.context import CryptContext
import os
from datetime import timedelta,timezone,datetime
from jose import jwt,JWTError
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas import Role_type
from models import Workspacealloc



pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt_handle_long_password=True
    )


SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
TOKEN_EXPIRE_MINUTES=30

def hashed_passowrd(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=[ALGORITHM])


def decode(token:str)->Optional[dict]:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None


oauth2_schema=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db))->User:
    credentail_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="crednetial validation error",
        headers={"WWW-Authenticate":"Bearer"},
        )
    
    try:
        payload=decode(token)

        if not payload:
            raise credentail_exception
        user_id:str=payload.get("sub")
        if not user_id:
            raise credentail_exception
        
    except (JWTError, ValueError):
        raise credentail_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user not found")
      
    return user  

def require_owner(current_user:User=Depends(get_current_user)):
    if current_user.role_type!=Role_type.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="data not found"
                            )
    return get_current_user   


def workspace_access(workspace_id:int,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    allocation=db.query(Workspacealloc).filter(Workspacealloc.user_id==current_user.id,Workspacealloc.workspace_id==workspace_id).first()
    if not allocation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="value not found")
    return workspace_id