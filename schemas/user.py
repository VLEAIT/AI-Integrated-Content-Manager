from pydantic import BaseModel,EmailStr,field_validator,model_validator,Field
from typing import Optional
from enum import Enum
from datetime import datetime

class Role_type(str,Enum):
    owner="owner"
    creator="creator"
    sub_creator="sub_creator"

class UserBase(BaseModel):
    email:EmailStr
    user_name:str=Field(... , min_length=6,max_length=17)
    role_type:Role_type

    @field_validator("user_name")
    @classmethod
    def user_n(cls,val:str)->str:
        val=val.strip()
        if " " in val:
            raise ValueError("space not allowed between username")
        return val

class UserCreate(UserBase):
    password:str=Field(min_length=8,max_length=15)
    confirm_password:str=Field(min_length=8,max_length=15)
    @model_validator(mode="after")
    def pass_val(self)->"UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("passport not matched")
        return self

class UserResponse(UserBase):
    id:int
    created_at:datetime
    model_config={"from_attributes":True}

class UserLogin(BaseModel):
    email:EmailStr
    password:str    

class UserUpdate(BaseModel):
    email:Optional[EmailStr]=None
    user_name:Optional[str]=None
    role_type:Optional[Role_type]=None

    @field_validator("user_name")
    @classmethod
    def name_val(cls,v:Optional[str])->Optional[str]:
        if v is None:
            return v
        v=v.strip()
        if " " in v:
            raise ValueError("space not allowed")
        return v
   

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    user_id:str=Field(default=None)    

class UserPasswordUpdate(BaseModel):
    old_password:str=Field(default=None)
    new_password:str=Field(default=None)

