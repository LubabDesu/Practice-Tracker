# in main.py (or routes/pieces.py)
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import select, Session as DBSession
from pydantic import BaseModel, Field
from typing import Optional, List
from ..db import get_db
from ..models import Piece, User
from ..security import get_current_user # the helper that reads your JWT cookie

router = APIRouter(prefix="/pieces", tags=['pieces'])

class PieceIn(BaseModel):
    title: str = Field(..., min_length=1)
    composer: Optional[str] = None
    difficulty: Optional[str] = None
    notes: Optional[str] = None

class PieceOut(PieceIn):
    id: int

@router.post("", response_model=PieceOut)
def create_piece(
    body: PieceIn,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    piece = Piece(owner_id=user.id, **body.model_dump())
    db.add(piece)
    db.commit()
    db.refresh(piece)
    return PieceOut(id=piece.id, **body.model_dump())


@router.get("", response_model=List[PieceOut])
def list_pieces(
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    rows = db.exec(select(Piece).where(Piece.owner_id == user.id).order_by(Piece.created_at.desc())).all()
    return [PieceOut(id=p.id, title=p.title, composer=p.composer, difficulty=p.difficulty, notes=p.notes) for p in rows]