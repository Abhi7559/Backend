from schemas.review import ReviewCreate, ReviewUpdate


def get_film_reviews(film_id: int) -> dict:
    return {"message": "Film reviews placeholder", "film_id": film_id}


def create_film_review(film_id: int, review_data: ReviewCreate) -> dict:
    return {"message": "Create review placeholder", "film_id": film_id}


def update_review(review_id: int, review_data: ReviewUpdate) -> dict:
    return {"message": "Update review placeholder", "review_id": review_id}


def delete_review(review_id: int) -> dict:
    return {"message": "Delete review placeholder", "review_id": review_id}
