from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.api.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


# =========================
# 🔍 GET PENDING USERS
# =========================
@router.get("/pending-users")
def get_pending_users(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin)   # ✅ FIXED
):
    users = db.query(models.User).filter(
        models.User.approval_status == "PENDING"
    ).all()

    print("🔥 Pending users:", users)  # DEBUG

    return users


# =========================
# ✅ APPROVE USER
# =========================
@router.put("/approve/{user_id}")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin)   # ✅ FIXED
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.approval_status = "ACTIVE"
    db.commit()

    return {"msg": "User approved"}
