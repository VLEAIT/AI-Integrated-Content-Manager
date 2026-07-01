from sqlalchemy import String,Enum,Text
from sqlalchemy.orm import relationship,mapped_column,Mapped
from sqlalchemy.sql import func
from database import Base,TimestampMixin
from schemas import Role_type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.workspace import Workspace
    from models.workspacealloc import Workspacealloc

class User(Base,TimestampMixin):
    __tablename__="users"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_name:Mapped[str]=mapped_column(String(17),index=True,nullable=False,unique=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    role_type:Mapped[Role_type]=mapped_column(Enum(Role_type),nullable=False)
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    workspaces:Mapped[list["Workspace"]]=relationship(back_populates="owner")
    workspace_alloc:Mapped[list["Workspacealloc"]]=relationship(back_populates="user")


