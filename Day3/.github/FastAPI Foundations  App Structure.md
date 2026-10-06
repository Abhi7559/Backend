# FastAPI Foundations + App Structure

## Exercise: Film Review Platform — API Skeleton

### Objective

Build a simple **FastAPI API skeleton** for a Film Review Platform.

The main purpose of this exercise is to practice FastAPI foundations and understand how a production-style application can be separated into layers:

**Routes → Handlers → Services → DAOs**

At this stage, the application does **not** need a real database or complete business logic.

The focus is on creating a clean project structure, registering routers, defining API endpoints, using request/response models, and understanding the application lifecycle.

## Important Implementation Rules

* Use **Python** with **FastAPI**.
* Use **uv** to manage the project and dependencies.
* Keep the code **simple and beginner-friendly**.
* Do not use unnecessary advanced Python features.
* Do not over-engineer the project.
* Use clear and meaningful file and folder names.
* Add type hints where they make the code easier to understand.
* Use Pydantic models for request and response data.
* Do not add a real database.
* DAO functions can return simple placeholder data.
* Do not add authentication logic yet.
* Do not add JWT implementation yet.
* Do not add complex business logic.
* Do not create a `tests` folder.
* Do not install or use `pytest`.
* Every required endpoint must exist and return a clearly labelled placeholder response.
* The application must start successfully using:

```bash
uv run uvicorn app.main:app --reload
```

## 1. Project Structure

Create the following structure:

```text
film-review-platform/
│
├── .github/
│   └── film-review-platform.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── films.py
│   │   ├── reviews.py
│   │   └── users.py
│   │
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── film_handler.py
│   │   ├── review_handler.py
│   │   └── user_handler.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── film_service.py
│   │   ├── review_service.py
│   │   └── user_service.py
│   │
│   ├── daos/
│   │   ├── __init__.py
│   │   ├── film_dao.py
│   │   ├── review_dao.py
│   │   └── user_dao.py
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── film.py
│       ├── review.py
│       └── user.py
│
├── pyproject.toml
└── uv.lock
```

The names should make the responsibility of each layer obvious.

## 2. Layer Responsibilities

Follow this architecture strictly:

```text
Client
  ↓
Routes
  ↓
Handlers
  ↓
Services
  ↓
DAOs
  ↓
Database
```

There is no real database in this exercise.

### Routes

The `routes` layer is responsible for:

* Defining API URLs.
* Defining HTTP methods.
* Reading path parameters.
* Reading query parameters.
* Reading request bodies.
* Declaring response models.
* Calling the appropriate handler.

Routes should **not** contain business logic.

Example:

```python
@router.get("/films")
def get_films():
    return film_handler.get_films()
```

### Handlers

The `handlers` layer receives the request-related information from routes and passes it to the service layer.

Handlers should remain simple.

Example:

```python
def get_films():
    return film_service.get_films()
```

### Services

The `services` layer is responsible for application/business logic.

For this exercise, keep it very simple.

Example:

```python
def get_films():
    return film_dao.get_films()
```

### DAOs

The `daos` layer is responsible for **direct data access only**.

For this exercise, there is no database.

Therefore, DAO functions can return simple placeholder data.

Example:

```python
def get_films():
    return []
```

Important rule:

> No route, handler, or service should directly access the database.

All direct database access must be inside the DAO layer.

## 3. Dependencies

Use:

* FastAPI
* Uvicorn

Add them using `uv`.

The project must be runnable with:

```bash
uv run uvicorn app.main:app --reload
```

Do not add unnecessary dependencies.

## 4. Main FastAPI Application

Create:

```text
app/main.py
```

The file must:

1. Create the FastAPI application.
2. Register the application lifespan.
3. Include the films router.
4. Include the reviews router.
5. Include the users router.
6. Create the public health-check endpoint.

Use a versioned API prefix:

```text
/api/v1
```

The final API structure should look like:

```text
/api/v1/films
/api/v1/films/{film_id}
/api/v1/films/{film_id}/reviews
/api/v1/reviews/{review_id}
/api/v1/auth/register
/api/v1/auth/login
/api/v1/users/me
/api/v1/admin/stats
```

The health endpoint can be:

```text
/health
```

It should remain outside the `/api/v1` prefix.

## 5. APIRouter

Use `APIRouter` to separate endpoints by domain.

Create three router modules:

```text
app/routes/films.py
app/routes/reviews.py
app/routes/users.py
```

Each router should have a clear tag.

Example:

```python
router = APIRouter(
    prefix="/films",
    tags=["Films"],
)
```

The main application should register the routers.

Example:

```python
app.include_router(films.router, prefix="/api/v1")
```

Use the same version prefix for all three routers.

## 6. Films Endpoints

Create the following endpoints:

```text
GET    /api/v1/films
GET    /api/v1/films/{film_id}
POST   /api/v1/films
PATCH  /api/v1/films/{film_id}
DELETE /api/v1/films/{film_id}
```

Every endpoint must exist.

At this stage, they should return simple placeholder responses.

Example:

```json
{
  "message": "Film list placeholder"
}
```

For the film ID endpoint, use the path parameter:

```text
GET /api/v1/films/10
```

Return something clearly labelled, such as:

```json
{
  "message": "Film details placeholder",
  "film_id": 10
}
```

## 7. Film Request Model

Create a simple Pydantic model in:

```text
app/schemas/film.py
```

Example fields:

```text
title
description
release_year
genre
```

Keep the model simple.

For example:

```python
class FilmCreate(BaseModel):
    title: str
    description: str
    release_year: int
    genre: str
```

The POST endpoint should accept this model as the request body.

Example request:

```json
{
  "title": "Inception",
  "description": "A science-fiction film",
  "release_year": 2010,
  "genre": "Sci-Fi"
}
```

The endpoint can return a placeholder response.

## 8. Film PATCH Model

Create a simple update model.

Fields should be optional so the client can update only the required fields.

Example:

```python
class FilmUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None
```

The PATCH endpoint should accept:

```text
PATCH /api/v1/films/{film_id}
```

and return a placeholder response containing the `film_id`.

## 9. Reviews Endpoints

Create:

```text
GET    /api/v1/films/{film_id}/reviews
POST   /api/v1/films/{film_id}/reviews
PATCH  /api/v1/reviews/{review_id}
DELETE /api/v1/reviews/{review_id}
```

Use the `film_id` path parameter for the first two endpoints.

Example:

```text
GET /api/v1/films/10/reviews
```

Return:

```json
{
  "message": "Film reviews placeholder",
  "film_id": 10
}
```

## 10. Review Request Model

Create:

```text
app/schemas/review.py
```

Use a simple Pydantic model.

Example:

```python
class ReviewCreate(BaseModel):
    rating: int
    comment: str
```

The POST review endpoint should accept the model as the request body.

Example:

```json
{
  "rating": 5,
  "comment": "Excellent movie!"
}
```

The review update endpoint should use a simple update model.

## 11. Auth and Users Endpoints

The users router should contain these endpoints:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
GET  /api/v1/admin/stats
```

Keep authentication simple.

Do **not** implement:

* JWT
* OAuth
* Password hashing
* Sessions
* Database authentication

Return clearly labelled placeholder responses.

Examples:

```json
{
  "message": "Register placeholder"
}
```

```json
{
  "message": "Login placeholder"
}
```

```json
{
  "message": "Current user placeholder"
}
```

```json
{
  "message": "Admin statistics placeholder"
}
```

## 12. User Schema

Create:

```text
app/schemas/user.py
```

Create a simple Pydantic model for registration.

Example:

```python
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
```

The login endpoint can use:

```python
class LoginRequest(BaseModel):
    email: str
    password: str
```

Do not implement real authentication.

## 13. Path Parameters

Use FastAPI path parameters for IDs.

Example:

```python
@router.get("/{film_id}")
def get_film(film_id: int):
    ...
```

FastAPI should automatically validate that `film_id` is an integer.

Use path parameters for:

```text
film_id
review_id
```

## 14. Query Parameters

At least one endpoint should demonstrate a query parameter.

Use the film list endpoint.

Example:

```text
GET /api/v1/films?genre=action
```

The route can be:

```python
@router.get("")
def get_films(genre: str | None = None):
    ...
```

Return the received value in the placeholder response.

Example:

```json
{
  "message": "Film list placeholder",
  "genre": "action"
}
```

The query parameter should be optional.

## 15. Request Bodies

Use Pydantic models for request bodies.

For example:

```python
@router.post("")
def create_film(film: FilmCreate):
    ...
```

FastAPI should automatically:

* Read the JSON request body.
* Validate the fields.
* Convert compatible types.
* Show the request schema in `/docs`.

## 16. Response Models

Use Pydantic response models for important endpoints.

Create simple response models inside the schemas.

For example:

```python
class MessageResponse(BaseModel):
    message: str
```

If an endpoint returns an ID:

```python
class FilmPlaceholderResponse(BaseModel):
    message: str
    film_id: int
```

Use:

```python
@router.get(
    "/{film_id}",
    response_model=FilmPlaceholderResponse,
)
```

Response models are required because they:

* Define the expected response structure.
* Validate returned data.
* Improve serialization.
* Automatically improve OpenAPI documentation.
* Make the API contract easier to understand.

Keep response models simple.

## 17. Health Check

Create a public health endpoint:

```text
GET /health
```

No authentication is required.

It should return:

* API status.
* Current server timestamp.

Example:

```json
{
  "status": "ok",
  "timestamp": "2026-09-24T12:30:00+00:00"
}
```

Use Python's standard library for the timestamp.

Example:

```python
from datetime import datetime, timezone

datetime.now(timezone.utc)
```

Do not add a separate dependency for this.

## 18. Application Lifespan

Use FastAPI's `lifespan` mechanism.

Do **not** use the deprecated:

```python
@app.on_event("startup")
@app.on_event("shutdown")
```

Create a lifespan function using an async context manager.

Example structure:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    yield
    print("Application shutting down")
```

Pass it to the FastAPI application:

```python
app = FastAPI(lifespan=lifespan)
```

The startup log should clearly indicate that the application has started.

The shutdown log should clearly indicate that the application is shutting down.

Keep the logging simple.

## 19. OpenAPI Documentation

FastAPI automatically provides interactive API documentation.

After starting the application:

```bash
uv run uvicorn app.main:app --reload
```

Open:

```text
/docs
```

The documentation should show all required endpoints.

The endpoints should be grouped using tags:

```text
Films
Reviews
Auth / Users
Health
```

Use router tags to prevent the API documentation from becoming one flat list.

The `/docs` page should show:

* HTTP methods.
* Paths.
* Path parameters.
* Query parameters.
* Request body schemas.
* Response schemas.
* Endpoint descriptions where useful.

Do not manually create an OpenAPI JSON file.

FastAPI should generate the OpenAPI documentation automatically from:

* Route definitions.
* Type hints.
* Pydantic schemas.
* Response models.

## 20. DAO Layer

The DAO layer must contain all direct data-access operations.

For example:

```text
app/daos/film_dao.py
app/daos/review_dao.py
app/daos/user_dao.py
```

There is no database in this exercise.

Therefore, DAO methods can return placeholder values.

Example:

```python
def get_films():
    return []
```

The important concept is the separation:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
DAO
```

Do not access DAO functions directly from routes.

For example, avoid:

```python
@router.get("/films")
def get_films():
    return film_dao.get_films()
```

Instead:

```text
Route → Handler → Service → DAO
```

## 21. Simple Data Flow Example

For:

```text
GET /api/v1/films
```

the flow should be:

```text
Client
  ↓
films.py route
  ↓
film_handler.py
  ↓
film_service.py
  ↓
film_dao.py
  ↓
placeholder data
  ↓
Response
```

For:

```text
POST /api/v1/films
```

the flow should be:

```text
Client
  ↓
JSON request
  ↓
FilmCreate Pydantic model
  ↓
films.py route
  ↓
film_handler.py
  ↓
film_service.py
  ↓
film_dao.py
  ↓
placeholder response
```

## 22. Expected API Surface

The final application must contain exactly these required API areas.

### Health

```text
GET /health
```

### Films

```text
GET    /api/v1/films
GET    /api/v1/films/{film_id}
POST   /api/v1/films
PATCH  /api/v1/films/{film_id}
DELETE /api/v1/films/{film_id}
```

### Reviews

```text
GET    /api/v1/films/{film_id}/reviews
POST   /api/v1/films/{film_id}/reviews
PATCH  /api/v1/reviews/{review_id}
DELETE /api/v1/reviews/{review_id}
```

### Auth / Users

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
GET  /api/v1/admin/stats
```

Total required endpoints:

```text
14 endpoints
```

## 23. Placeholder Response Requirement

Every endpoint must return a response that makes its purpose obvious.

Do not return vague responses such as:

```json
{
  "message": "Hello"
}
```

Prefer:

```json
{
  "message": "Film list placeholder"
}
```

or:

```json
{
  "message": "Delete film placeholder",
  "film_id": 10
}
```

This makes it easy to understand and test the API skeleton.

## 24. Code Quality Requirements

Keep the code:

* Simple.
* Readable.
* Beginner-friendly.
* Properly formatted.
* Consistent.
* Type hinted where useful.
* Split according to the specified layers.

Avoid:

* Complex abstractions.
* Generic repository frameworks.
* Dependency injection frameworks.
* Unnecessary design patterns.
* Real authentication.
* Real database integration.
* JWT.
* OAuth.
* Complex error handling.
* Unnecessary third-party packages.

The goal is to learn **FastAPI foundations and application structure**, not to build the complete film platform.

## 25. README Requirement

Do not create a README specifically for explaining the architecture.

The folder and file names must already make the responsibilities clear.

The Markdown specification itself is the source of truth for the exercise.

## 26. Verification

After implementation, run:

```bash
uv run uvicorn app.main:app --reload
```

Verify that the application starts without errors.

Open:

```text
http://127.0.0.1:8000/docs
```

Verify that all required endpoints appear.

Also verify:

```text
GET /health
```

returns the API status and current timestamp.

Verify that:

```text
GET /api/v1/films
```

works with and without the optional query parameter:

```text
/api/v1/films
```

and:

```text
/api/v1/films?genre=action
```

Verify that POST endpoints accept JSON request bodies and that the schemas are visible in `/docs`.

## Final Goal

By completing this exercise, the project should demonstrate that you understand:

1. What FastAPI is.
2. How a FastAPI application is structured.
3. How `APIRouter` separates API domains.
4. How routes are registered in the main application.
5. How path parameters work.
6. How query parameters work.
7. How request bodies work with Pydantic.
8. How response models work.
9. How FastAPI generates OpenAPI documentation.
10. How `/docs` provides interactive API documentation.
11. How application lifespan handles startup and shutdown.
12. Why the DAO layer owns direct database access.
13. Why Routes → Handlers → Services → DAOs provides clear separation of responsibilities.

The implementation should be a **clean API skeleton**, not a fully functional film review platform.
