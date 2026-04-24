from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.chat_ws import router as ws_router

# DB IMPORTS
from backend.app.db.database import engine
from backend.app.db import models

app = FastAPI()

# ✅ FORCE DB TABLE CREATION HERE
models.Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)

@app.get("/")
def root():
    return {"msg": "API running"}
