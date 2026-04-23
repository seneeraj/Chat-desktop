from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.chat_ws import router as ws_router
from backend.app.api.routes.admin import router as admin_router

# ✅ CREATE APP FIRST (VERY IMPORTANT)
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ CORS (FIXED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔥 allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 📁 FILE UPLOAD STATIC
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ==============================
# ROUTES
# ==============================
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)
app.include_router(admin_router)

# ==============================
# ROOT
# ==============================
@app.get("/")
def root():
    return {"msg": "API running"}
    
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)   
