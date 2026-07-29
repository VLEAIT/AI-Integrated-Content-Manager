from sqlalchemy import create_engine,Column,DateTime
from sqlalchemy.orm  import sessionmaker,DeclarativeBase,Mapped,mapped_column,MappedAsDataclass
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.sql import func


import os


load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
    )

SessionLocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

class TimestampMixin:
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    

class Base(MappedAsDataclass,DeclarativeBase,kw_only=True):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()  



