from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db import models, schemas
from backend.app.core.security import create_access_token
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # Admin logic
    if user.username.lower() == "admin":
        role = "ADMIN"
        status = "ACTIVE"
    else:
        role = "USER"
        status = "PENDING"

    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed,
        role=role,
        approval_status=status
    )

    db.add(db_user)
    db.commit()

    return {"msg": "Signup successful"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    print("🔥 LOGIN HIT:", user.username)

    # Get user from DB
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check approval
    if db_user.approval_status != "ACTIVE":
        raise HTTPException(status_code=403, detail="User not approved")

    # Check password
    if not bcrypt.checkpw(user.password.encode(), db_user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Wrong password")

    # 🔥 CREATE TOKEN (FIXED)
    token = create_access_token({
        "user_id": db_user.id,
        "username": db_user.username,   # ✅ IMPORTANT FIX
        "role": db_user.role
    })

    return {
        "access_token": token,
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "role": db_user.role
        }
    }