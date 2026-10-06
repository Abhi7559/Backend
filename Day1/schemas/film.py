from pydantic import BaseModel


class FilmCreate(BaseModel):
    title: str
    description: str
    release_year: int
    genre: str


class FilmUpdate(FilmCreate):
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None


class FilmPlaceholderResponse(BaseModel):
    message: str
    film_id: int


class FilmListPlaceholderResponse(BaseModel):
    message: str
    genre: str | None = None
