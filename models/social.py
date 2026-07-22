from sqlalchemy import column,Integer,String,Text,ForeignKey,Enum,Boolean,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from database import Base
from schemas import platform_opt
from datetime import datetime
from sqlalchemy.sql import func

class SocialAccount(Base):
    __tablename__="social_accounts"

    id:Mapped[int]=mapped_column(Integer,nullable=False,primary_key=True,index=True)
    workspace_id:Mapped[int]=mapped_column(Integer,ForeignKey("workspace.id",ondelete="CASCADE"),nullable=False)
    platform:Mapped[platform_opt]=mapped_column(Enum(platform_opt),nullable=False)
    account_name:Mapped[str]=mapped_column(String,nullable=False)
    access_token:Mapped[str]=mapped_column(String,nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
