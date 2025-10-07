# app/routes/sessions.py
from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlmodel import Session as DBSession, select, col

from app.db import get_db
from app.models import PracticeSession, Piece, User
from app.security import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

# ---------- Schemas ----------
class SessionIn(BaseModel):
    piece_id: int
    practice_date: date
    minutes: int = Field(ge=1, le=600)
    focus: Optional[str] = Field(default=None, max_length=120)
    notes: Optional[str] = Field(default=None, max_length=1000)

class SessionOut(SessionIn):
    id: int

    # Optional: pretty output check
    @field_validator("practice_date", mode="before")
    @classmethod
    def coerce_date(cls, v):
        # allow "YYYY-MM-DD" strings
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v

# ---------- Routes ----------

@router.post("", response_model=SessionOut)
def create_session(
    body: SessionIn,
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Ownership check: piece must belong to this user
    piece = db.exec(
        select(Piece).where(
            Piece.id == body.piece_id,
            Piece.owner_id == user.id,
        )
    ).first()
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found or not owned by user")

    row = PracticeSession(
        user_id=user.id,
        piece_id=body.piece_id,
        practice_date=body.practice_date,
        minutes=body.minutes,
        focus=body.focus,
        notes=body.notes,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return SessionOut(
        id=row.id,
        piece_id=row.piece_id,
        practice_date=row.practice_date,
        minutes=row.minutes,
        focus=row.focus,
        notes=row.notes,
    )


@router.get("", response_model=List[SessionOut])
def list_sessions(
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
    piece_id: Optional[int] = Query(default=None, description="Filter by piece"),
    date_from: Optional[date] = Query(default=None, description="Inclusive start (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(default=None, description="Inclusive end (YYYY-MM-DD)"),
):
    q = select(PracticeSession).where(PracticeSession.user_id == user.id)

    if piece_id is not None:
        # Ensure the piece belongs to the user
        owned = db.exec(select(Piece.id).where(Piece.id == piece_id, Piece.owner_id == user.id)).first()
        if not owned:
            raise HTTPException(status_code=404, detail="Piece not found or not owned by user")
        q = q.where(PracticeSession.piece_id == piece_id)

    if date_from is not None:
        q = q.where(PracticeSession.practice_date >= date_from)
    if date_to is not None:
        q = q.where(PracticeSession.practice_date <= date_to)

    q = q.order_by(col(PracticeSession.practice_date).desc(), col(PracticeSession.id).desc())
    rows = db.exec(q).all()

    return [
        SessionOut(
            id=r.id,
            piece_id=r.piece_id,
            practice_date=r.practice_date,
            minutes=r.minutes,
            focus=r.focus,
            notes=r.notes,
        )
        for r in rows
    ]