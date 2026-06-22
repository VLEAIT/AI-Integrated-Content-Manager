from sqlalchemy import Column,Text,String,Integer,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship,mapped_column,Mapped
from sqlalchemy.sql import func
from database import Base
from schemas import Role_type
from enum import Enum

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_name:Mapped[str]=mapped_column(String(17),index=True,nullable=False,unique=True)
    email:Mapped[str]=mapped_column(String(20),unique=True,nullable=False)
    role_type:Mapped[Role_type]=mapped_column(Enum(Role_type),nullable=False)
    hashed_password:Mapped[str]=mapped_column(String(15),nullable=False)
    created_at=Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now())

    


        