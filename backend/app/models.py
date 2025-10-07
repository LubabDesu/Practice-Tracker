from __future__ import annotations
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    display_name: Optional[str] = None
    picture_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Piece(SQLModel, table=True):
    __tablename__ = "pieces"
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id")   # FK to users
    title: str
    composer: Optional[str] = None
    difficulty: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PracticeSession(SQLModel, table=True):
    __tablename__ = "practice_sessions"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    piece_id: int = Field(foreign_key="pieces.id")
    practice_date: date
    minutes: int
    focus: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)