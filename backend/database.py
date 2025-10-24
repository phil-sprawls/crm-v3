from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# Add connection pooling with pre-ping to handle dropped connections
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args, 
    echo=True,
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=10,        # Connection pool size
    max_overflow=20      # Allow up to 20 overflow connections
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
