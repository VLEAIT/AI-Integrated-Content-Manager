from pydantic import BaseModel,Field,HttpUrl
from datetime import datetime
from enum import Enum
from typing import Literal,Optional

class platform_opt(str,Enum):
    instagram="instagram"
    tiktok="tiktok"
    facebook="facebook"

class PostMasterBase(BaseModel):
    content_url:HttpUrl=Field(... , description="claude storage link")
    raw_description:str=Field(...  ,description="the descirption of value")

class PostMasterCreate(PostMasterBase):
    workspace_id:int

class PostMasterResponse(PostMasterBase):
    id:int
    workspace_id:int
    creator_id:int
    ai_caption:Optional[str]=None
    created_at:datetime    

    model_config={"from_attributes":True}

class PostChildBase(BaseModel):
    platform:platform_opt

class PostChildCreate(PostChildBase):
    scheduled_time:Optional[datetime]=None    

class PostChildResponse(PostChildBase):
    id:int
    masterpost_id:int
    approval_status:Literal["pending","approved","rejected"]="pending"
    is_published:bool=False
    boost_budget:float=0.0
    published_at:Optional[datetime]=None
    scheduled_time:Optional[datetime]=None

    model_config={"from_attributes":True}


class MegaPostSubmission(BaseModel):
    master:PostMasterCreate
    target_platfotrm:list[platform_opt]    


  

