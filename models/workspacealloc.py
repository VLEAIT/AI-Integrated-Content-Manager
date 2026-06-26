from sqlalchemy import ForeignKey
from sqlalchemy.orm  import Mapped,mapped_column,relationship
from database import Base,TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.workspace import Workspace


class Workspacealloc(Base,TimestampMixin):
    __tablename__="workspacealloc"

    id:Mapped[int]=mapped_column(primary_key=True)
    workspace_id:Mapped[int]=mapped_column(ForeignKey("workspace.id", ondelete="CASCADE"),nullable=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),nullable=True)
    can_approve_posts:Mapped[bool]=mapped_column(default=False,nullable=False)
    can_access_ai:Mapped[bool]=mapped_column(default=False,nullable=False)

    user :Mapped["User"]=relationship(back_populates="workspace_allc")
    workspaceall:Mapped["Workspace"]=relationship(back_populates="memeber_alloc")

