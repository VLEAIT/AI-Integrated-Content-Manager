from passlib.context import CryptContext
import os
from datetime import timedelta,timezone,datetime
from jose import jwt,JWTError
from typing import Optional







pwd_context=CryptContext(
    schemes="bcrypt",
    deprecated="auto",
    bcrypt_handle_long_password=True
    )


SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="H256"
TOKEN_EXPIRE_MINUTES=30

def hashed_passowrd(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def decode(token:str)->Optional[dict]:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    except JWTError:
        return None



