from pydantic import BaseModel,Field

class WorkBase(BaseModel):
    brand_name:str=Field(min_length=2,max_length=16)
    require_approval:bool=Field(True)


class WorkResponse(WorkBase):
    id:int
    created_at=int
    owner_id=int

          