from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.api.auth import router as auth_router
from app.api.wells import router as wells_router
from app.api.alerts import router as alerts_router
from app.api.ws import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="WellGuard API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(wells_router)
app.include_router(alerts_router)
app.include_router(ws_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "WellGuard API"}
