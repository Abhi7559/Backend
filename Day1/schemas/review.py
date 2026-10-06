from pydantic import BaseModel


class ReviewCreate(BaseModel):
    rating: int
    comment: str


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None


class ReviewPlaceholderResponse(BaseModel):
    message: str
    review_id: int


class FilmReviewPlaceholderResponse(BaseModel):
    message: str
    film_id: int
