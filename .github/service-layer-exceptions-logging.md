# Exercise: Film Review Platform — Service Layer, Centralized Exceptions & Structured Logging

## Goal

Extend the existing Film Review Platform by adding:

1. `FilmService`
2. `ReviewService`
3. Custom domain exceptions
4. Centralized FastAPI exception handling
5. Structured JSON logging
6. Request-scoped `request_id` in every log entry

Keep the implementation **simple, beginner-friendly, and easy to understand**.

Do not introduce unnecessary libraries, abstractions, or complicated patterns.

## Important Existing Architecture

The project already has:

```text
Route → Handler → DAO → Database
```

Change it to:

```text
Route → Handler → Service → DAO → Database
```

The responsibilities must remain clear:

### Route

Only define the API endpoint and connect dependencies.

### Handler

Handle request/response concerns.

Handlers should call services.

Handlers must NOT contain business rules.

### Service

Contains business logic and domain rules.

Services can call DAOs.

Services must NOT directly execute SQLAlchemy database queries.

### DAO

The DAO is the only layer that directly accesses the database.

Do not move database logic into services.

---

# Part 1 — Inspect the Existing Project First

Before changing code:

1. Inspect the complete project structure.
2. Find the existing:

   * Film model
   * Review model
   * User model
   * Film DAO
   * Review DAO
   * User DAO
   * Film routes
   * Review routes
   * Handlers
   * Pydantic schemas
   * FastAPI application setup
   * Database session dependency
   * Existing request ID implementation from Day 3
   * Existing logging configuration, if any
3. Understand the existing naming conventions.
4. Reuse existing code instead of creating duplicate implementations.
5. Do not change existing route signatures unless absolutely necessary.
6. Do not remove working functionality.

After inspecting the project, implement the following requirements.

---

# Part 2 — Add the Service Layer

Create a service layer using the project's existing folder structure.

Prefer something similar to:

```text
services/
├── film_service.py
└── review_service.py
```

If the project already has a different service folder structure, follow the existing structure instead.

---

# Part 3 — FilmService

Create `FilmService`.

It should use the existing `FilmDAO` and `ReviewDAO`.

Example responsibility:

```text
FilmService
    ↓
FilmDAO
ReviewDAO
```

Implement the film-related business operations that already exist in the application.

At minimum, support:

* Get film
* List films
* Create film
* Update film
* Soft delete film

Do not put direct database queries inside `FilmService`.

---

# Part 4 — Film Soft Delete Rule

Implement this business rule:

> A film cannot be soft-deleted while it still has active reviews.

For this exercise, define an active review as:

```text
review.is_active == True
```

If the existing Review model uses another field to represent deletion/active state, reuse the existing field instead of adding a duplicate field.

Before soft-deleting a film:

```text
1. Find the film.
2. If film does not exist:
       raise FilmNotFoundError

3. Check whether the film has active reviews.

4. If active reviews exist:
       raise FilmHasActiveReviewsError

5. Otherwise:
       soft-delete the film.
```

Do not physically delete the film if the existing application uses soft deletion.

---

# Part 5 — ReviewService

Create `ReviewService`.

It should use the existing:

```text
ReviewDAO
FilmDAO
UserDAO
```

only when necessary.

Implement:

* Create review
* Get review
* Update review

Follow the existing project method signatures and schemas where possible.

---

# Part 6 — Business Rule: One Review Per User Per Film

Implement this rule:

> A user may not submit more than one review for the same film.

When creating a review:

```text
1. Check whether the film exists.
2. Check whether the user already reviewed the film.
3. If an existing review is found:
       raise DuplicateReviewError
4. Otherwise:
       create the review.
```

Example:

```text
User 1 + Film 5
        ↓
Already reviewed?
        ↓
      YES
        ↓
DuplicateReviewError
```

Do not enforce this rule inside the route or handler.

It belongs in `ReviewService`.

---

# Part 7 — Business Rule: Review Owner

Implement this rule:

> A review's rating and body may only be updated by the user who originally wrote the review.

When updating a review:

```text
1. Find the review.
2. If it does not exist:
       raise ReviewNotFoundError

3. Compare:
       review.user_id
       current_user.id

4. If they are different:
       raise UnauthorisedReviewAccessError

5. Otherwise:
       update rating/body.
```

Example:

```text
Review 10
Owner = User 1

User 1 → update → allowed

User 2 → update → rejected
```

Do not put this authorization/business rule inside the route.

---

# Part 8 — Custom Domain Exceptions

Create a domain exception module.

Prefer something similar to:

```text
exceptions/
└── domain.py
```

Create a common base exception:

```python
class DomainError(Exception):
    pass
```

Then create these exceptions:

```text
FilmNotFoundError
ReviewNotFoundError
DuplicateReviewError
UnauthorisedReviewAccessError
FilmHasActiveReviewsError
```

Each exception must contain:

1. A typed identifier for the affected resource.
2. A clear human-readable message.

For example:

```python
class FilmNotFoundError(DomainError):
    def __init__(self, film_id: int):
        self.film_id = film_id
        super().__init__(f"Film {film_id} was not found.")
```

Another example:

```python
class ReviewNotFoundError(DomainError):
    def __init__(self, review_id: int):
        self.review_id = review_id
        super().__init__(f"Review {review_id} was not found.")
```

For duplicate review:

```python
class DuplicateReviewError(DomainError):
    def __init__(self, user_id: int, film_id: int):
        self.user_id = user_id
        self.film_id = film_id
        super().__init__(
            f"User {user_id} has already reviewed film {film_id}."
        )
```

For unauthorized access:

```python
class UnauthorisedReviewAccessError(DomainError):
    def __init__(self, review_id: int, user_id: int):
        self.review_id = review_id
        self.user_id = user_id
        super().__init__(
            f"User {user_id} is not allowed to modify review {review_id}."
        )
```

For active reviews:

```python
class FilmHasActiveReviewsError(DomainError):
    def __init__(self, film_id: int):
        self.film_id = film_id
        super().__init__(
            f"Film {film_id} cannot be deleted because it has active reviews."
        )
```

Keep the exceptions simple.

Do not create unnecessary exception hierarchies.

---

# Part 9 — Centralized Exception Handling

Create centralized exception handlers.

Prefer:

```text
exceptions/
├── domain.py
└── handlers.py
```

Register the handlers on the FastAPI application.

Example concept:

```python
@app.exception_handler(ReviewNotFoundError)
async def review_not_found_handler(request, exc):
    ...
```

Do NOT put domain-specific `try/except` blocks in every route.

Bad:

```python
try:
    service.update_review(...)
except ReviewNotFoundError:
    ...
```

Do not do this.

Instead:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
raise DomainError
  ↓
FastAPI centralized exception handler
  ↓
JSON response
```

---

# Part 10 — Error Response Format

Every domain exception must return the same JSON structure:

```json
{
  "type": "ReviewNotFoundError",
  "message": "Review 10 was not found.",
  "detail": {
    "review_id": 10
  }
}
```

The fields are:

```text
type
message
detail
```

Use the exception's typed attributes to populate `detail`.

Examples:

### Film not found

```json
{
  "type": "FilmNotFoundError",
  "message": "Film 10 was not found.",
  "detail": {
    "film_id": 10
  }
}
```

### Duplicate review

```json
{
  "type": "DuplicateReviewError",
  "message": "User 1 has already reviewed film 5.",
  "detail": {
    "user_id": 1,
    "film_id": 5
  }
}
```

### Unauthorized review update

```json
{
  "type": "UnauthorisedReviewAccessError",
  "message": "User 2 is not allowed to modify review 10.",
  "detail": {
    "review_id": 10,
    "user_id": 2
  }
}
```

---

# Part 11 — HTTP Status Codes

Use these status codes:

```text
FilmNotFoundError
    → 404

ReviewNotFoundError
    → 404

DuplicateReviewError
    → 409

UnauthorisedReviewAccessError
    → 403

FilmHasActiveReviewsError
    → 409
```

Use `JSONResponse` or the project's existing response approach.

Keep the implementation consistent.

---

# Part 12 — Structured JSON Logging

Configure application logging so every log entry is JSON.

Each log entry must contain at minimum:

```text
level
timestamp
logger
message
request_id
```

Example:

```json
{
  "level": "INFO",
  "timestamp": "2026-10-05T17:30:00+05:30",
  "logger": "app.services.review_service",
  "message": "Review created successfully.",
  "request_id": "abc-123"
}
```

Do not use only:

```python
print("Review created")
```

Use Python's logging system.

For example:

```python
logger.info("Review created successfully.")
```

---

# Part 13 — Logging Levels

Use logging levels appropriately.

Use:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

For this exercise, mainly use:

```text
DEBUG
INFO
WARNING
ERROR
```

Examples:

```text
INFO
Review created successfully.

INFO
Film updated successfully.

WARNING
User attempted to modify another user's review.

ERROR
Unexpected database/service error.
```

Do not add logs to every line of code.

Log meaningful events.

---

# Part 14 — Request ID Logging Context

The project already has a request trace identifier from Day 3.

Reuse the existing implementation.

Do not create a second request ID system unless the existing implementation is missing.

Every log produced during one request must contain the same request ID.

For example:

```json
{
  "level": "INFO",
  "timestamp": "...",
  "logger": "app.handlers.review",
  "message": "Received review creation request.",
  "request_id": "req-123"
}
```

Then:

```json
{
  "level": "INFO",
  "timestamp": "...",
  "logger": "app.services.review_service",
  "message": "Checking for existing review.",
  "request_id": "req-123"
}
```

And:

```json
{
  "level": "INFO",
  "timestamp": "...",
  "logger": "app.services.review_service",
  "message": "Review created successfully.",
  "request_id": "req-123"
}
```

All three logs have:

```text
request_id = req-123
```

---

# Part 15 — Logger Usage

Create module-level loggers where appropriate.

Example:

```python
import logging

logger = logging.getLogger(__name__)
```

Then:

```python
logger.info("Review created successfully.")
```

Do not use `print()` for application logging.

---

# Part 16 — Service Logging

Add useful logs to `FilmService` and `ReviewService`.

Examples:

### Review creation

```text
INFO:
Creating review for film 5 by user 10.
```

### Duplicate review

```text
WARNING:
User 10 already reviewed film 5.
```

### Review update

```text
INFO:
Updating review 15.
```

### Unauthorized update

```text
WARNING:
User 20 attempted to modify review 15 owned by another user.
```

### Film deletion blocked

```text
WARNING:
Film 5 cannot be deleted because active reviews exist.
```

Do not log passwords, tokens, or sensitive user information.

---

# Part 17 — Exception Handler Logging

When a domain exception is handled, log it appropriately.

Example:

```text
WARNING:
ReviewNotFoundError handled.
```

Include:

```text
request_id
```

The client response should remain the consistent JSON structure defined above.

---

# Part 18 — Thin Handlers

After implementation, inspect the handlers.

They should look conceptually like:

```python
async def create_review(...):
    return await review_service.create_review(...)
```

They should NOT contain:

```text
duplicate review checking
ownership checking
active review checking
database queries
domain try/except blocks
```

Those belong elsewhere.

---

# Part 19 — Dependency Injection

Use the project's existing FastAPI dependency injection pattern.

If DAOs are already injected using:

```python
Depends(...)
```

continue using that approach.

Services can receive DAOs through dependency injection.

Keep the dependency chain simple:

```text
Request
 ↓
Handler
 ↓
ReviewService
 ↓
ReviewDAO
 ↓
Database
```

Do not create global database sessions.

Do not create database sessions manually inside services.

---

# Part 20 — Do Not Break Existing APIs

Preserve existing:

* Routes
* Request schemas
* Response schemas
* Database models
* DAO interfaces

unless a change is genuinely required by this exercise.

Do not rename public API endpoints unnecessarily.

Do not rewrite working code just for style.

---

# Part 21 — Testing the Exercise Manually

After implementation, verify these scenarios.

## Test 1 — Create Review

```text
User 1
Film 1

First review
→ should succeed
```

## Test 2 — Duplicate Review

```text
User 1
Film 1

Second review
→ should return 409
```

Expected:

```json
{
  "type": "DuplicateReviewError",
  "message": "...",
  "detail": {
    "user_id": 1,
    "film_id": 1
  }
}
```

## Test 3 — Update Own Review

```text
Review owner = User 1
Current user = User 1

→ should succeed
```

## Test 4 — Update Someone Else's Review

```text
Review owner = User 1
Current user = User 2

→ should return 403
```

## Test 5 — Delete Film With Active Review

```text
Film 1
Active review exists

→ should return 409
```

## Test 6 — Delete Film Without Active Reviews

```text
Film 1
No active reviews

→ soft delete should succeed
```

## Test 7 — Missing Review

```text
GET /reviews/99999
```

→ should return `404`.

## Test 8 — Logging

Make at least one request and verify the application logs contain JSON objects with:

```text
level
timestamp
logger
message
request_id
```

Verify that logs generated during the same request contain the same request ID.

---

# Part 22 — Code Quality Requirements

Keep the implementation beginner-friendly.

Follow these rules:

* Use clear class names.
* Use type hints.
* Use simple functions.
* Keep services focused.
* Keep handlers thin.
* Keep DAOs responsible for database access.
* Do not put SQLAlchemy queries inside services.
* Do not put business rules inside routes.
* Do not use `print()` for application logs.
* Do not add unnecessary abstractions.
* Do not add unnecessary dependencies.
* Do not change unrelated code.
* Do not create duplicate database sessions.
* Do not use domain `try/except` blocks in route handlers.

---

# Part 23 — Final Architecture

The completed application should conceptually look like:

```text
                         FastAPI
                            │
                            ↓
                       Request ID
                            │
                            ↓
                          Route
                            │
                            ↓
                         Handler
                            │
                            ↓
                         Service
                       ↙         ↘
                  Business      Logger
                    Rules          │
                       ↓           ↓
                      DAO       JSON Logs
                       ↓
                   PostgreSQL
```

For errors:

```text
Service
   │
   │ raises
   ↓
Domain Exception
   │
   ↓
Central Exception Handler
   │
   ↓
Consistent JSON Response
```

---

# Part 24 — Final Deliverable

After implementation:

1. Run the application.
2. Confirm it starts successfully.
3. Confirm existing endpoints still work.
4. Verify the service layer is being used.
5. Verify business rules work.
6. Verify domain exceptions work.
7. Verify centralized exception handlers work.
8. Verify JSON error responses contain:

   * `type`
   * `message`
   * `detail`
9. Verify logs are JSON.
10. Verify every log contains:

    * `level`
    * `timestamp`
    * `logger`
    * `message`
    * `request_id`
11. Run the project's existing type checker/linter.
12. Fix all errors introduced by this implementation.

At the end, provide a short summary containing:

```text
Files created
Files modified
Business rules implemented
Exception mappings
Logging implementation
How request_id is propagated
Commands used to run/check the application
```

Keep the summary simple and beginner-friendly.
