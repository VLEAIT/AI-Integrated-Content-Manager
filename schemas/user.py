from pydantic import BaseModel,EmailStr,field_validator,model_validator,Field
from typing import List
from enum import Enum
from datetime import datetime

class role_type(str,Enum):
    owner="owner"
    creator="creator"
    sub_creator="sub_creator"

class UserBase(BaseModel):
    email:EmailStr
    user_name:str=Field(min_length=6,max_length=17)
    role_type:role_type

    @field_validator("user_name")
    @classmethod
    def user_n(cls,val:str)->str:
        val=val.strip()
        if " " in val:
            raise ValueError("space not allowed between")
        return val

class UserCreate(UserBase):
    password:str=Field(min_length=8,max_length=15)
    conform_passport:str=Field(min_lenth=8,max_length=15)
    @model_validator(model="after")
    def pass_val(self):
        if self.password != self.conform_passport:
            raise ValueError("passport not matched")
        return self

class UserResponse(UserBase):
    id:int
    created_at:int
    model_config={"from_attributes":True}

class UserLogin(BaseModel):
    email:EmailStr
    password:str    





