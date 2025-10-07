from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlmodel import select
from app.db import get_db
from app.models import User
from sqlmodel import Session as DBSession
import os

# Load environment secret
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
COOKIE_NAME = os.getenv("COOKIE_NAME", "pt_session")

# -------------------------------
# 1. Helper to extract email from JWT
# -------------------------------
def get_user_email(request: Request) -> str:
    """Extracts and verifies the JWT from the user's cookie, returning the email (sub)."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing subject")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# -------------------------------
# 2. Optional: get_user_name (if you want to display it)
# -------------------------------
def get_user_name(request: Request) -> str:
    """Temporary placeholder — name can be retrieved later from DB if needed."""
    return request.cookies.get("user_name", "Guest")

# -------------------------------
# 3. Real get_current_user — returns full User object
# -------------------------------
def get_current_user(
    request: Request,
    db: DBSession = Depends(get_db)
) -> User:
    """Returns the User object corresponding to the current JWT-authenticated user."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth cookie")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        # if you want, you could auto-create here; but better to require login flow to create
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user