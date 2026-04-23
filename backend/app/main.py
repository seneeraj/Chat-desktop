from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.chat_ws import router as ws_router

app = FastAPI(
    title="Chat Backend API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)

# ✅ Root test
@app.get("/")
def root():
    return {"msg": "API running"}
