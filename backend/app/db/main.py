from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api.routes import auth

app.include_router(auth.router)


app = FastAPI()

# 🔥 This line creates tables automatically
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg": "API running"}