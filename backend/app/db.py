"""
Read the address from your .env file and establish a robust connection to the database
"""

import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL", "sqlite:///./piano.db")
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)

def init_db() :
    from .models import User, Piece, PracticeSession
    SQLModel.metadata.create_all(engine)

# with Session(engine) opens a transaction-safe connection for the lifetime 
# of the request, then closes it.
def get_db():
    with Session(engine) as db:
        yield db