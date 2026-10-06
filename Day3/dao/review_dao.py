from datetime import datetime, timezone
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate


def get_film_reviews(film_id: int) -> dict:
    print(f"[Review DAO] Fetching reviews for film ID: {film_id}")
    return {"message": "Reviews retrieved successfully", "film_id": film_id}


def create_film_review(film_id: int, review_data: ReviewCreate) -> ReviewResponse:
    print(f"[Review DAO] Creating review for film ID: {film_id} with rating: {review_data.rating}")

    # Simulated review creation with auto-generated id, reviewer name, and current UTC timestamp
    return ReviewResponse(
        id=1,
        film_id=film_id,
        rating=review_data.rating,
        body=review_data.body,
        reviewer_name="Abhishek",
        submitted_at=datetime.now(timezone.utc),
    )


def update_review(review_id: int, review_data: ReviewUpdate) -> dict:
    print(f"[Review DAO] Updating review ID: {review_id}")
    return {
        "message": "Review updated successfully",
        "review_id": review_id,
        "updated_fields": review_data.model_dump(exclude_unset=True),
    }


def delete_review(review_id: int) -> dict:
    print(f"[Review DAO] Deleting review ID: {review_id}")
    return {"message": "Review deleted successfully", "review_id": review_id}
