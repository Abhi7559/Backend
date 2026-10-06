from schemas.film import FilmCreate, FilmResponse, FilmUpdate
from services import film_service


def get_films(genre: str | None = None) -> dict:
    return film_service.get_films(genre=genre)


def get_film_by_id(film_id: int) -> dict:
    return film_service.get_film_by_id(film_id)


def create_film(film_data: FilmCreate) -> FilmResponse:
    return film_service.create_film(film_data)


def update_film(film_id: int, film_data: FilmUpdate) -> dict:
    return film_service.update_film(film_id, film_data)


def delete_film(film_id: int) -> dict:
    return film_service.delete_film(film_id)
