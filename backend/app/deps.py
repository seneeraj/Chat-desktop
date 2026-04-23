from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


# ==============================
# 🔐 GET CURRENT USER ID
# ==============================
def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id   # ✅ RETURN ONLY INTEGER

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ==============================
# 👑 GET CURRENT ADMIN
# ==============================
def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")

        if user_id is None or role != "ADMIN":
            raise HTTPException(status_code=403, detail="Admin access required")

        return user_id   # ✅ return admin user_id

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")