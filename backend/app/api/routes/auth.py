from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from backend.app.db.database import get_db
from backend.app.db import models, schemas
from backend.app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):

    # ✅ Check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # ✅ Hash password
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # ✅ Admin logic
    if user.username.lower() == "admin":
        role = "ADMIN"
        status = "ACTIVE"
    else:
        role = "USER"
        status = "PENDING"

    # ✅ Create user
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed,
        role=role,
        approval_status=status
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)   # ✅ important

    return {
        "msg": "Signup successful",
        "user_id": db_user.id
    }


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    print("🔥 LOGIN HIT:", user.username)


    users = db.query(models.User).all()
    print("🔥 ALL USERS IN DB:", [(u.id, u.username, u.email) for u in users])

    

    # ✅ SUPPORT BOTH username OR email (robust)
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.username)
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Approval check
    if db_user.approval_status != "ACTIVE":
        raise HTTPException(status_code=403, detail="User not approved")

    # ✅ Password check
    if not bcrypt.checkpw(user.password.encode(), db_user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Wrong password")

    # ✅ Create token
    token = create_access_token({
        "user_id": db_user.id,
        "username": db_user.username,
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
