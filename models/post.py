from sqlalchemy import ForeignKey,String,Text,Enum,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship        
from database import Base,TimestampMixin
from schemas import platform_opt
from schemas import status
from datetime import datetime
from typing import List,Optional

class PostMasterModel(Base,TimestampMixin):
    __tablename__="post_master"
    id:Mapped[int]=mapped_column(primary_key=True)
    workspace_id:Mapped[int]=mapped_column(ForeignKey("workspace.id", ondelete="CASCADE"),nullable=True)
    creator_id:Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=True)
    content_url:Mapped[str]=mapped_column(Text,nullable=False)
    raw_description:Mapped[str]=mapped_column(Text,nullable=False)
    ai_caption:Mapped[Optional[str]]=mapped_column(Text,nullable=False)

    children:Mapped[List["PostChildModel"]]=relationship(back_populates="master", cascade="all, delete-orphan")



class PostChildModel(Base,TimestampMixin):
    __tablename__="post_child"
    id:Mapped[int]=mapped_column(primary_key=True)
    masterpost_id:Mapped[int]=mapped_column(ForeignKey("post_master.id",ondelete="CASCADE"),nullable=False)
    platform:Mapped[platform_opt]=mapped_column(Enum(platform_opt),nullable=False)
    approval_status:Mapped[status]=mapped_column(Enum(status),nullable=False)
    is_published:Mapped[bool]=mapped_column(default=False, nullable=False)
    boost_budget:Mapped[float]=mapped_column(default=0.0,nullable=False)
    scheduled_time:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=None)
    published_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=None)


    master:Mapped["PostMasterModel"]=relationship(back_populates="children")
