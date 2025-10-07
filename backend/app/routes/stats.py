# app/routes/stats.py
from __future__ import annotations
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlmodel import select, func
from sqlmodel import Session as DBSession

from app.db import get_db
from app.models import PracticeSession, Piece, User
from app.security import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/overview")
def overview(
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = date.today()
    start7 = today - timedelta(days=6)

    # total minutes last 7 days
    total_7 = db.exec(
        select(func.coalesce(func.sum(PracticeSession.minutes), 0))
        .where(PracticeSession.user_id == user.id,
               PracticeSession.practice_date >= start7)
    ).one()

    # top piece by minutes (last 7 days)
    top = db.exec(
        select(Piece.title, func.sum(PracticeSession.minutes).label("m"))
        .join(Piece, Piece.id == PracticeSession.piece_id)
        .where(PracticeSession.user_id == user.id,
               PracticeSession.practice_date >= start7)
        .group_by(Piece.title)
        .order_by(func.sum(PracticeSession.minutes).desc())
    ).first()

    # streak: consecutive days ending today with any practice
    days = db.exec(
        select(PracticeSession.practice_date)
        .where(PracticeSession.user_id == user.id,
               PracticeSession.practice_date <= today)
        .group_by(PracticeSession.practice_date)
        .order_by(PracticeSession.practice_date.desc())
    ).all()
    dayset = set(days)
    streak = 0
    d = today
    while d in dayset:
        streak += 1
        d -= timedelta(days=1)

    return {
        "total_minutes_last_7_days": int(total_7 or 0),
        "top_piece_last_7_days": top[0] if top else None,
        "current_streak_days": streak,
    }

# Optional: minutes per day (for charts)
@router.get("/by-day")
def by_day(
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
    days: int = 14,
):
    start = date.today() - timedelta(days=days - 1)
    rows = db.exec(
        select(PracticeSession.practice_date,
               func.sum(PracticeSession.minutes))
        .where(PracticeSession.user_id == user.id,
               PracticeSession.practice_date >= start)
        .group_by(PracticeSession.practice_date)
        .order_by(PracticeSession.practice_date.asc())
    ).all()
    return [{"date": str(d), "minutes": int(m)} for d, m in rows]