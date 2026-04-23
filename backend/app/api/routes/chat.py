import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from backend.app.db.database import get_db
from backend.app.db import models
from backend.app.api.deps import get_current_user
from backend.app.core.encryption import decrypt_message

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

router = APIRouter(prefix="/chat", tags=["Chat"])


# ==============================
# 🔑 HELPER: SAFE USER ID
# ==============================
def extract_user_id(user):
    if isinstance(user, dict):
        return user.get("user_id")
    return user


# ==============================
# 🔐 SAFE DECRYPT
# ==============================
def safe_decrypt(value):
    try:
        return decrypt_message(value) if value else ""
    except Exception as e:
        print("❌ Decryption Error:", e)
        return "[Decryption Failed]"


# ==============================
# 👤 GET USERS
# ==============================
@router.get("/users")
def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_id = extract_user_id(user)

    users = db.query(models.User).filter(
        models.User.id != user_id
    ).all()

    return users


# ==============================
# 📩 GET MESSAGES (FIXED)
# ==============================
@router.get("/messages/{receiver_id}")
def get_messages(
    receiver_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_id = extract_user_id(user)

    messages = db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == user_id, models.Message.receiver_id == receiver_id),
            and_(models.Message.sender_id == receiver_id, models.Message.receiver_id == user_id)
        )
    ).order_by(models.Message.timestamp.asc()).all()

    print(f"📥 Loaded {len(messages)} messages between {user_id} and {receiver_id}")

    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "message": safe_decrypt(m.encrypted_message),
            "file_url": m.file_url,
            "file_type": m.file_type,
            "status": getattr(m, "status", "SENT"),
            "timestamp": str(m.timestamp)
        }
        for m in messages
    ]


# ==============================
# 📁 FILE UPLOAD
# ==============================
UPLOAD_DIR = "uploads"

# Ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        # ✅ SAFE FILE NAME
        safe_filename = file.filename.replace(" ", "_")

        # ✅ UNIQUE FILE NAME
        unique_name = f"{uuid.uuid4()}_{safe_filename}"

        file_path = os.path.join(UPLOAD_DIR, unique_name)

        # ✅ SAVE FILE
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ FILE TYPE DETECTION
        if file.content_type and "image" in file.content_type:
            file_type = "image"
        elif file.content_type and "pdf" in file.content_type:
            file_type = "pdf"
        else:
            file_type = "file"

        return {
            "file_url": f"{BASE_URL}/uploads/{unique_name}",
            "file_type": file_type,
            "file_name": safe_filename 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))