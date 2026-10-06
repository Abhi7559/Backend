from dao import review_dao
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate


def get_film_reviews(film_id: int) -> dict:
    return review_dao.get_film_reviews(film_id)


def create_film_review(film_id: int, review_data: ReviewCreate) -> ReviewResponse:
    return review_dao.create_film_review(film_id, review_data)


def update_review(review_id: int, review_data: ReviewUpdate) -> dict:
    return review_dao.update_review(review_id, review_data)


def delete_review(review_id: int) -> dict:
    return review_dao.delete_review(review_id)
