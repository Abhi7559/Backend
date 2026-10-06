from schemas.film import FilmCreate, FilmUpdate


def get_films(genre: str | None = None) -> dict:
    if genre:
        return {"message": "Film list placeholder", "genre": genre}
    return {"message": "Film list placeholder"}


def get_film_by_id(film_id: int) -> dict:
    return {"message": "Film details placeholder", "film_id": film_id}


def create_film(film_data: FilmCreate) -> dict:
    return {"message": "Create film placeholder"}


def update_film(film_id: int, film_data: FilmUpdate) -> dict:
    return {"message": "Update film placeholder", "film_id": film_id,"update_film":film_data}


def delete_film(film_id: int) -> dict:
    return {"message": "Delete film placeholder", "film_id": film_id}
