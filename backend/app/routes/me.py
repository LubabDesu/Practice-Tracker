# User profile endpoint
from __future__ import annotations
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select, func
from sqlmodel import Session as DBSession

from ..db import get_db
from ..models import User, Piece, PracticeSession
from ..security import get_current_user

router = APIRouter(prefix="/me", tags=["me"])

class MeOverview(BaseModel):
    email: str
    display_name: str | None = None
    picture_url: str | None = None
    joined_on: date | None = None

    total_pieces: int
    total_sessions: int
    total_minutes: int

    last_practice_date: date | None = None
    current_streak_days: int
    longest_streak_days: int

@router.get("", response_model=MeOverview)
def me(
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Aggregate counts + minutes
    pieces_count = db.exec(
        select(func.count()).select_from(Piece).where(Piece.owner_id == user.id)
    ).one()

    sessions_count = db.exec(
        select(func.count()).select_from(PracticeSession).where(PracticeSession.user_id == user.id)
    ).one()

    minutes_total = db.exec(
        select(func.coalesce(func.sum(PracticeSession.minutes), 0))
        .where(PracticeSession.user_id == user.id)
    ).one()

    # Distinct practice days (for streaks)
    days = db.exec(
        select(PracticeSession.practice_date)
        .where(PracticeSession.user_id == user.id)
        .group_by(PracticeSession.practice_date)
        .order_by(PracticeSession.practice_date.asc())
    ).all()

    # Basic metadata
    last_date = days[-1] if days else None

    # Streaks
    day_set = set(days)
    today = date.today()

    # current streak (count back from today)
    cur_streak = 0
    d = today
    while d in day_set:
        cur_streak += 1
        d -= timedelta(days=1)

    # longest streak (scan all dates)
    longest = 0
    if days:
        run = 1
        for i in range(1, len(days)):
            if days[i] == days[i-1] + timedelta(days=1):
                run += 1
            else:
                longest = max(longest, run)
                run = 1
        longest = max(longest, run)

    return MeOverview(
        email=user.email,
        display_name=user.display_name,
        picture_url=user.picture_url,
        joined_on=(user.created_at.date() if getattr(user, "created_at", None) else None),

        total_pieces=int(pieces_count or 0),
        total_sessions=int(sessions_count or 0),
        total_minutes=int(minutes_total or 0),

        last_practice_date=last_date,
        current_streak_days=cur_streak,
        longest_streak_days=longest,
    )