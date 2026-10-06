from typing import Any
from fastapi import APIRouter, Depends

from core.config import Settings
from dependencies.auth import get_current_user
from dependencies.config import get_config
from dependencies.database import get_db
from dependencies.trace import get_trace_id
from handlers import film_handler
from schemas.film import FilmCreate, FilmResponse, FilmUpdate, ReleaseWindow

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get("")
def get_films(
    genre: str | None = None,
    config: Settings = Depends(get_config),
    db: dict[str, Any] = Depends(get_db),
    trace_id: str = Depends(get_trace_id),
):
    """
    Retrieve all films.
    Declares all three shared dependencies: config, db, and trace_id.
    """
    films_data = film_handler.get_films(genre=genre)
    return {
        "message": "Films retrieved successfully",
        "api_version": config.API_VERSION,
        "trace_id": trace_id,
        "database": db,
        "data": films_data,
    }


@router.get("/{film_id}")
def get_film(
    film_id: int,
    config: Settings = Depends(get_config),
    db: dict[str, Any] = Depends(get_db),
    trace_id: str = Depends(get_trace_id),
    current_user: dict[str, Any] = Depends(get_current_user),
):
    """
    Retrieve a film by ID.
    Declares all three shared dependencies PLUS the current-user dependency (demonstrating dependency chaining).
    """
    film_data = film_handler.get_film_by_id(film_id)
    return {
        "message": f"Film {film_id} details retrieved successfully",
        "api_version": config.API_VERSION,
        "trace_id": trace_id,
        "database": db,
        "current_user": current_user,
        "data": film_data,
    }


@router.post("", response_model=FilmResponse, status_code=201)
def create_film(film: FilmCreate):
    return film_handler.create_film(film)


@router.patch("/{film_id}")
def update_film(film_id: int, film: FilmUpdate):
    return film_handler.update_film(film_id, film)


@router.delete("/{film_id}")
def delete_film(film_id: int):
    return film_handler.delete_film(film_id)


@router.post("/filter-by-window")
def filter_films_by_window(window: ReleaseWindow):
    """
    Filter films within a release year window.
    Demonstrates ReleaseWindow cross-field validation in Swagger UI.
    """
    return {
        "message": f"Filtering films between {window.start_year} and {window.end_year}",
        "start_year": window.start_year,
        "end_year": window.end_year,
    }

