from schemas.film import FilmCreate, FilmResponse, FilmUpdate


def get_films(genre: str | None = None) -> dict:
    print(f"[Film DAO] Fetching films list. Genre filter: {genre}")
    if genre:
        return {"message": "Films retrieved successfully", "genre": genre}
    return {"message": "All films retrieved successfully"}


def get_film_by_id(film_id: int) -> dict:
    print(f"[Film DAO] Fetching film by ID: {film_id}")
    return {"message": "Film details retrieved successfully", "film_id": film_id}


def create_film(film_data: FilmCreate) -> FilmResponse:
    print(f"[Film DAO] Creating new film record: '{film_data.title}' ({film_data.release_year})")
    
    # We simulate saving a new film with an auto-generated id (id=1).
    # Pydantic v2 automatically calculates the computed field 'years_ago' based on 'release_year'.
    return FilmResponse(
        id=1,
        title=film_data.title,
        release_year=film_data.release_year,
        genre=film_data.genre,
        director=film_data.director,
    )


def update_film(film_id: int, film_data: FilmUpdate) -> dict:
    print(f"[Film DAO] Updating film ID: {film_id}")
    return {
        "message": "Film updated successfully",
        "film_id": film_id,
        "updated_fields": film_data.model_dump(exclude_unset=True),
    }


def delete_film(film_id: int) -> dict:
    print(f"[Film DAO] Deleting film ID: {film_id}")
    return {"message": "Film deleted successfully", "film_id": film_id}
