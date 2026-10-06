from fastapi import APIRouter

from handlers import film_handler
from schemas.film import FilmCreate, FilmPlaceholderResponse, FilmResponse, FilmUpdate

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get("")
def get_films(genre: str | None = None):
    return film_handler.get_films(genre=genre)


@router.get("/{film_id}", response_model=FilmPlaceholderResponse)
def get_film(film_id: int):
    return film_handler.get_film_by_id(film_id)


@router.post("", response_model=FilmResponse, status_code=201)
def create_film(film: FilmCreate):
    return film_handler.create_film(film)


@router.patch("/{film_id}")
def update_film(film_id: int, film: FilmUpdate):
    return film_handler.update_film(film_id, film)


@router.delete("/{film_id}")
def delete_film(film_id: int):
    return film_handler.delete_film(film_id)
