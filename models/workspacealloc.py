from sqlalchemy import ForeignKey,Enum
from sqlalchemy.orm  import Mapped,mapped_column,relationship
from database import Base,TimestampMixin
from typing import TYPE_CHECKING
from schemas import Role_type

if TYPE_CHECKING:
    from models.user import User
    from models.workspace import Workspace


class Workspacealloc(Base,TimestampMixin):
    __tablename__="workspacealloc"

    id:Mapped[int]=mapped_column(primary_key=True)
    workspace_id:Mapped[int]=mapped_column(ForeignKey("workspace.id", ondelete="CASCADE"),nullable=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=True)
    can_approve_posts:Mapped[bool]=mapped_column(default=False,nullable=False)
    can_access_ai:Mapped[bool]=mapped_column(default=False,nullable=False)
    allocated_role:Mapped[Role_type]=mapped_column(Enum(Role_type),nullable=False)

    user :Mapped["User"]=relationship(back_populates="workspace_alloc")
    workspaceall:Mapped["Workspace"]=relationship(back_populates="member_alloc")

