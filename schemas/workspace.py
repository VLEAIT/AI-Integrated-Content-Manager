from pydantic import BaseModel,Field
from typing import List
from enum import Enum

class role_type(str,Enum)
    owner="owner"
    creator="creator"
    sub_creator="sub_creator"

class WorkBase(BaseModel):
    brand_name:str=Field(min_length=2,max_length=16)
    require_approval:bool=Field(True)


class WorkBaseCreate(WorkBase):
    pass


class WorkBaseMember(BaseModel):
    user_id:int
    username:str
    role_type:role_type
    can_approve_posts:bool=False


class WorkResponse(WorkBase):
    id:int
    created_at:int
    owner_id:int
    require_approval:bool
    aloocated_members:List[WorkBaseMember]

          