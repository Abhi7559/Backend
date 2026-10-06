from dao import film_dao
from schemas.film import FilmCreate, FilmResponse, FilmUpdate


def get_films(genre: str | None = None) -> dict:
    return film_dao.get_films(genre=genre)


def get_film_by_id(film_id: int) -> dict:
    return film_dao.get_film_by_id(film_id)


def create_film(film_data: FilmCreate) -> FilmResponse:
    return film_dao.create_film(film_data)


def update_film(film_id: int, film_data: FilmUpdate) -> dict:
    return film_dao.update_film(film_id, film_data)


def delete_film(film_id: int) -> dict:
    return film_dao.delete_film(film_id)
