from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from typing import TYPE_CHECKING
from database import Base,TimestampMixin

class PostMasterModel(Base,TimestampMixin):
    id:Mapped[int]=mapped_column(primary_key=True)
    workspace_id:Mapped[int]=mapped_column(ForeignKey("workspace.id", ondelete="CASCADE"),nullable=True)