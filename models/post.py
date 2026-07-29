from sqlalchemy import ForeignKey,String,Text,Enum as SQLEnum,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship        
from database import Base,TimestampMixin
from schemas import platform_opt
from schemas import statu
from datetime import datetime
from typing import List,Optional
from enum import Enum




class AIstatus(str,Enum):
    QUEUED="queued"
    PROCESSING="processing"
    COMPLETED="completed"
    FAILED="failed"

class PostMasterModel(Base,TimestampMixin):
    __tablename__="post_master"
    id:Mapped[int]=mapped_column(primary_key=True)
    workspace_id:Mapped[int]=mapped_column(ForeignKey("workspace.id", ondelete="CASCADE"),nullable=True)
    creator_id:Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=True)
    content_url:Mapped[str]=mapped_column(Text,nullable=False)
    raw_description:Mapped[str]=mapped_column(Text,nullable=False)
    ai_caption:Mapped[Optional[str]]=mapped_column(Text,nullable=True)
    caption_ai_status:Mapped[AIstatus]=mapped_column(SQLEnum(AIstatus),default=AIstatus.QUEUED,nullable=False)
    caption_ai_error:Mapped[Optional[str]]=mapped_column(Text,nullable=True)
 

    children:Mapped[List["PostChildModel"]]=relationship(back_populates="master", cascade="all, delete-orphan")



class PostChildModel(Base,TimestampMixin):
    __tablename__="post_child"
    id:Mapped[int]=mapped_column(primary_key=True,init=False)
    masterpost_id:Mapped[int]=mapped_column(ForeignKey("post_master.id",ondelete="CASCADE"),nullable=False)
    platform:Mapped[platform_opt]=mapped_column(SQLEnum(platform_opt),nullable=False,init=False)
    approval_status:Mapped[statu]=mapped_column(SQLEnum(statu),default=statu.pending,init=False)
    is_published:Mapped[bool]=mapped_column(default=False, init=False)
    boost_budget:Mapped[float]=mapped_column(default=0.0,init=False)
    social_account_id:Mapped[int]=mapped_column(ForeignKey("social_accounts.id",ondelete="CASCADE"),nullable=False)
    scheduled_time:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=None)
    published_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=None)


    master:Mapped["PostMasterModel"]=relationship(back_populates="children")
