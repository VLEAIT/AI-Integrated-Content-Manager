from pydantic import BaseModel,Field
from typing import List
from datetime import datetime
from schemas.user import Role_type



class WorkBase(BaseModel):
    brand_name:str=Field(min_length=2,max_length=16)
    require_approval:bool=Field(True)


class WorkBaseCreate(WorkBase):
    pass


class WorkBaseMember(BaseModel):
    user_id:int
    username:str
    role_type:Role_type


class WorkResponse(WorkBase):
    id:int
    created_at:datetime
    owner_id:int
    allocated_members:List[WorkBaseMember]

    model_config={"from_attributes":True}

          