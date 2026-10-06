from fastapi import APIRouter

from handlers import review_handler
from schemas.review import ReviewCreate, ReviewUpdate

router = APIRouter(
    tags=["Reviews"],
)


@router.get("/films/{film_id}/reviews")
def get_film_reviews(film_id: int):
    return review_handler.get_film_reviews(film_id)


@router.post("/films/{film_id}/reviews")
def create_film_review(film_id: int, review: ReviewCreate):
    return review_handler.create_film_review(film_id, review)


@router.patch("/reviews/{review_id}")
def update_review(review_id: int, review: ReviewUpdate):
    return review_handler.update_review(review_id, review)


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    return review_handler.delete_review(review_id)
