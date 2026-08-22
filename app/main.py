from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import check_db_health, close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="OrchestraAI Backend",
    version="0.1.0",
    description="Backend service for OrchestraAI",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
async def database_health() -> dict[str, str]:
    is_healthy = await check_db_health()
    if is_healthy:
        return {"status": "healthy", "database": "connected"}
    return {"status": "unhealthy", "database": "disconnected"}
