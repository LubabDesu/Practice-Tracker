import os
from dotenv import load_dotenv

# 1) Load .env BEFORE importing modules that read env vars
load_dotenv()

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .db import init_db
from .auth import router as auth_router          # /login, /auth/callback, /logout
from .routes import pieces, sessions, me, stats  # your real /api/* routers

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI()

# Sessions needed for Authlib's request.session during OAuth
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS for your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Include routers (avoid duplicate /api/me definitions)
app.include_router(auth_router)
app.include_router(pieces.router,   prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(me.router,       prefix="/api")
app.include_router(stats.router,    prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()

# Optional: tiny root/index for manual testing
def get_user_name(request: Request):
    return request.cookies.get("user_name", "Guest")  # demo only; not your JWT

@app.get("/", response_class=HTMLResponse)
def home(user: str = Depends(get_user_name)):
    return f"""
    <html>
      <body>
        <h1>Hello, {user}!</h1>
        <a href="/login">Login with Google</a>
      </body>
    </html>
    """

@app.get("/api/health")
def health_check():
    return {"status": "ok"}