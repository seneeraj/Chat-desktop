from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ CORRECT IMPORTS (VERY IMPORTANT)
from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.chat_ws import router as ws_router

from backend.app.db.database import engine
from backend.app.db import models

# ✅ CREATE APP
app = FastAPI()

# ✅ CREATE TABLES
models.Base.metadata.create_all(bind=engine)

# ✅ ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ INCLUDE ROUTERS (THIS IS THE FIX)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)

# ✅ TEST ROUTE
@app.get("/")
def root():
    return {"msg": "API running"}
