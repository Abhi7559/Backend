import sys
from pathlib import Path

# Ensure directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI

from core.config import settings
from routes import films, reviews, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Application started - API Version: {settings.API_VERSION}")
    yield
    print("Application shutting down")


app = FastAPI(
    title="Film Review Platform API",
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Register routers under /api/v1 (or configurable API version)
api_prefix = f"/api/{settings.API_VERSION}"
app.include_router(films.router, prefix=api_prefix)
app.include_router(reviews.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "api_version": settings.API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
