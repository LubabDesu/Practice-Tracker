from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from .security import get_user_email, get_user_name
from .models import User, PracticeSession, Piece
from .db import get_db
from sqlmodel import select, Session as DBSession
import json



load_dotenv()
router = APIRouter()
oauth = OAuth()

# Setup OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
COOKIE_NAME = os.getenv("COOKIE_NAME", "pt_session")
BASE_URL_BACKEND = "http://localhost:8000"
BASE_URL_FRONTEND = "http://localhost:5173"
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

def frontend_url(path: str = "/") -> str:
    # ensure single slash join
    return FRONTEND_ORIGIN.rstrip("/") + "/" + path.lstrip("/")

# Register Google OAuth (OpenID Connect)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

def create_session_jwt(sub: str, minutes: int = 240) -> str:
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=minutes)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@router.get("/login")
async def login(request: Request):
    redirect_uri = f"{BASE_URL_BACKEND}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request, db: DBSession = Depends(get_db)):

    
    token = await oauth.google.authorize_access_token(request)
    next_path = "/"
    if "state" in token:
        try:
            next_path = json.loads(token["state"]).get("next", "/")
        except Exception:
            next_path = "/"
    userinfo = token.get("userinfo")
    if not userinfo and "id_token" in token:
        userinfo = jwt.get_unverified_claims(token["id_token"])
    if not userinfo:
        raise HTTPException(400, "Could not retrieve user info from Google")

    email = userinfo["email"]
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        user = User(email=email, display_name=name, picture_url=picture)
        db.add(user); db.commit(); db.refresh(user)

    session_jwt = create_session_jwt(email)
    target = frontend_url(next_path)
    resp = RedirectResponse(url=target, status_code=303) 
    resp.set_cookie(
        key=COOKIE_NAME,
        value=session_jwt,
        httponly=True,
        secure=False,  # set True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 4,
        path="/",
    )
    
    return resp

# @router.get("/api/me")
# async def get_user_profile(request: Request, 
#                            user_email: str = Depends(get_user_email), 
#                            user_name: str = Depends(get_user_name)) :
#     return User(name=user_name, email=user_email)

@router.get("/logout")
async def logout():
    resp = RedirectResponse(url=BASE_URL_FRONTEND)
    resp.delete_cookie(
        key=os.getenv("COOKIE_NAME", "pt_session"),
        path="/",
    )
    return resp