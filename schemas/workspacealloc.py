from pydantic import BaseModel
from datetime import datetime

class WorkAllocBase(BaseModel):
    workspace_id:int
    user_id:int
    can_approve_posts:bool=False
    can_access_ai:bool=False


class WorkAllocCreate(WorkAllocBase):
    pass

class WorkAllocResponse(WorkAllocBase):
    id:int
    assigned_at:datetime

    model_config={"from_attributes":True}
