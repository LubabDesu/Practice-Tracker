import os
from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuth
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .auth import router
from starlette.middleware.sessions import SessionMiddleware
from .db import init_db
from .routes import pieces, sessions, me, stats
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")




app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],              # exact Vercel URL
    allow_origin_regex=r"^https://.*\.vercel\.app$",  # allow previews too
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

api_router = APIRouter(prefix="/api", tags=["auth"])
app.include_router(api_router)
app.include_router(pieces.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(me.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.on_event("startup")
def on_startup() :
    init_db()

@api_router.get("/me") # Full path will be /api/me
def get_user_data():
    # ... logic to get user data from DB ...
    return {"name": "Lucas", "email": "lucas@example.com"} # Returns JSON

@app.get("/api/health")
def health_check():
    # It's good practice to have a simple health check endpoint
    return {"status": "ok"}

def get_user_name(request: Request):
    return request.cookies.get("user_name", "Guest")

@app.get("/", response_class=HTMLResponse)
def home(user: str = Depends(get_user_name)):
    return f"""
    <html>
        <head><title>FastAPI Google Auth Test</title></head>
        <body>
            <h1 style="color: blue; font-size: 24px">Hello, {user}!</h1>
            <a href="/login">Login with Google</a>
        </body>
    </html>
    """

@app.get("/me", response_class=HTMLResponse)
def protected_page(user: str = Depends(get_user_name)):
    return f"""
    <html>
        <head><title>My Profile</title></head>
        <body>
            <h1>Welcome to your profile, {user}!</h1>
            <p>You are successfully logged in.</p>
        </body>
    </html>
    """


# https://accounts.google.com/signin/oauth/error?authError=Cg5pbnZhbGlkX2NsaWVudBIfVGhlIE9BdXRoIGNsaWVudCB3YXMgbm90IGZvdW5kLiCRAw%3D%3D&
# client_id=None&flowName=GeneralOAuthFlow