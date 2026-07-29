from sqlalchemy import Integer,String,Text,ForeignKey,Enum as SQLEnum,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from database import Base,TimestampMixin
from schemas import platform_opt

class SocialAccount(Base,TimestampMixin):
    __tablename__="social_accounts"

    id:Mapped[int]=mapped_column(Integer,nullable=False,primary_key=True,index=True)
    workspace_id:Mapped[int]=mapped_column(Integer,ForeignKey("workspace.id",ondelete="CASCADE"),nullable=False)
    platform:Mapped[platform_opt]=mapped_column(SQLEnum(platform_opt,native_enum=False),nullable=False)
    account_name:Mapped[str]=mapped_column(String,nullable=False)
    platform_account_id:Mapped[str]=mapped_column(String,nullable=False)
    access_token:Mapped[str]=mapped_column(String,nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
   
