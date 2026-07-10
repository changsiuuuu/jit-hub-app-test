from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from .database import engine
from .models import Base
from .seed import seed_traffic
from .routers import traffic
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_traffic()
    yield


app = FastAPI(title="JIT-Hub Traffic Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "traffic",
        "location": settings.jithub_location,
        "timestamp": datetime.now(timezone.utc),
    }
