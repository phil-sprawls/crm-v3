from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
