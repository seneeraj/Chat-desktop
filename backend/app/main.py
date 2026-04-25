from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIXED IMPORTS
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router
from app.api.routes.chat_ws import router as ws_router

from app.db.database import engine
from app.db import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)

@app.get("/")
def root():
    return {"msg": "API running"}
