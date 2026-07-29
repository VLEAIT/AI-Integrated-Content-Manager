from sqlalchemy import Integer,String,ForeignKey
from database import Base,TimestampMixin
from sqlalchemy.orm import relationship,Mapped,mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from  models.user import User
    from models.workspacealloc import Workspacealloc

class Workspace(Base,TimestampMixin):
    __tablename__="workspace"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,init=False)
    brand_name:Mapped[str]=mapped_column(String(17),index=True,nullable=False)
    owner_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    
    owner:Mapped["User"]=relationship(back_populates="workspaces",init=False)
    member_alloc:Mapped[list["Workspacealloc"]]=relationship(back_populates="workspaceall",init=False)

