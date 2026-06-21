from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker,DeclarativeBase
from dotenv import load_dotenv

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

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    