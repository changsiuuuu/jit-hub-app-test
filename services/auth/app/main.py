from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from .database import engine
from .models import Base
from .routers import auth, internal
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="JIT-Hub Auth Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(internal.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "auth",
        "location": settings.jithub_location,
        "timestamp": datetime.now(timezone.utc),
    }
