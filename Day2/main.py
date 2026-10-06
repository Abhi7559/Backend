import sys
from pathlib import Path

# Ensure directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI

from routes import films, reviews, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    yield
    print("Application shutting down")


app = FastAPI(
    title="Film Review Platform API",
    lifespan=lifespan,
)

# Register routers under /api/v1
app.include_router(films.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
