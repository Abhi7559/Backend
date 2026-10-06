from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from services import review_service


def get_film_reviews(film_id: int) -> dict:
    return review_service.get_film_reviews(film_id)


def create_film_review(film_id: int, review_data: ReviewCreate) -> ReviewResponse:
    return review_service.create_film_review(film_id, review_data)


def update_review(review_id: int, review_data: ReviewUpdate) -> dict:
    return review_service.update_review(review_id, review_data)


def delete_review(review_id: int) -> dict:
    return review_service.delete_review(review_id)
