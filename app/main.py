from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from .database import engine
from .models import Base
from .routers import auth, service, weather, traffic, tourist
from .seed import run_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    run_all()
    yield


app = FastAPI(
    title="JIT-Hub API Service",
    description="Active-Standby 전환 메커니즘을 적용한 하이브리드 DR API 서비스",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(service.router)
app.include_router(weather.router)
app.include_router(traffic.router)
app.include_router(tourist.router)

# 정적 파일 (HTML)
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
static_path = os.path.abspath(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(static_path, "login.html"))
