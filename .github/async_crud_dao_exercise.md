# Async CRUD + DAO Pattern

## Exercise: Film Review Platform — DAO Layer

Implement the DAO layer for the existing Film Review Platform project.

The project already has FastAPI, PostgreSQL, SQLAlchemy async ORM, AsyncSession dependency, Film/Review/User models, schemas, and existing routes/services/handlers from previous exercises.

Before creating anything, inspect the existing project and reuse the existing models, schemas, database configuration, naming conventions, and imports. Do not create duplicate models, duplicate database configuration, or duplicate session factories.

## Main Goal

Move all direct database access into DAO classes.

The architecture MUST be:

```text
Route → Handler → Service → DAO → AsyncSession → PostgreSQL
```

Rules:

- Routes must not call DAOs directly.
- Handlers must not call DAOs directly.
- Services must call DAOs.
- Routes must call handlers.
- Handlers must call services.
- Only DAO classes may execute database queries.
- Every DAO method must receive `AsyncSession` as a parameter.
- DAO methods must never create their own database session.
- Use SQLAlchemy async APIs.
- Use complete type hints.

## 1. Inspect Existing Project

Before modifying files:

1. Inspect the project structure.
2. Find the existing Film, Review, and User ORM models.
3. Find the existing AsyncSession configuration and dependency.
4. Find existing schemas, routes, handlers, and services.
5. Reuse existing project conventions.
6. Do not rewrite unrelated code.
7. Do not add unnecessary dependencies.

## 2. Create DAO Package

If a DAO package does not already exist, create it using the existing application package structure:

```text
app/
└── daos/
    ├── __init__.py
    ├── film_dao.py
    ├── review_dao.py
    └── user_dao.py
```

Use the actual project package name if it differs.

## 3. FilmDAO

Create a typed asynchronous `FilmDAO` using the existing `Film` ORM model.

### Get Film by ID

Implement:

```python
async def get_by_id(
    self,
    session: AsyncSession,
    film_id: int,
) -> Film | None:
    ...
```

Requirements:

- Find one film by ID.
- Return the Film when found.
- Return `None` when not found.
- Do not raise a not-found exception from the DAO.
- Use the supplied AsyncSession.

### List Films

Implement:

```python
async def list(
    self,
    session: AsyncSession,
    genre: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
) -> list[Film]:
    ...
```

Requirements:

- Return a list of films.
- Apply genre filtering only when `genre` is provided.
- Apply lower-year filtering only when `year_from` is provided.
- Apply upper-year filtering only when `year_to` is provided.
- Support multiple filters together.
- Do not apply filters whose values are `None`.
- If the model contains `is_active`, only return active films.

### Create Film

Implement:

```python
async def create(
    self,
    session: AsyncSession,
    film: Film,
) -> Film:
    ...
```

Requirements:

- Add the film to the supplied session.
- Flush/refresh as appropriate.
- Return the created Film.
- Do not create another session.
- Follow the existing project's transaction/commit strategy.

### Update Film

Implement a typed method similar to:

```python
async def update(
    self,
    session: AsyncSession,
    film_id: int,
    data: FilmUpdate,
) -> Film | None:
    ...
```

Use the existing update schema if available. Create one only if necessary.

Requirements:

- Find the existing film.
- Return `None` if it does not exist.
- Update only fields actually provided.
- Do not overwrite unspecified fields with `None`.
- Persist the changes.
- Return the updated Film.

### Soft Delete Film

Implement:

```python
async def soft_delete(
    self,
    session: AsyncSession,
    film_id: int,
) -> bool:
    ...
```

Requirements:

- Do NOT physically delete the film row.
- Mark it inactive using the existing active/inactive field, preferably `is_active` if present.
- Return `True` when found and marked inactive.
- Return `False` when not found.
- Normal film listing must exclude inactive films if soft-delete support exists.

## 4. ReviewDAO

Create a typed asynchronous `ReviewDAO` using the existing Review model.

### List Reviews by Film

Implement:

```python
async def list_by_film(
    self,
    session: AsyncSession,
    film_id: int,
) -> list[Review]:
    ...
```

Requirements:

- Return reviews belonging to the film.
- Order by the actual submission/creation timestamp field.
- Most recent review first.
- Return an empty list when there are no reviews.

### Average Rating

Implement:

```python
async def average_rating(
    self,
    session: AsyncSession,
    film_id: int,
) -> float | None:
    ...
```

Requirements:

- Calculate the average rating using a database aggregate such as SQL `AVG`.
- Return the average when reviews exist.
- Return `None` when there are no reviews.
- Do not return `0` for no reviews.

### Create Review

Implement:

```python
async def create(
    self,
    session: AsyncSession,
    review: Review,
) -> Review:
    ...
```

Requirements:

- Add the review to the supplied session.
- Flush/refresh as appropriate.
- Return the created Review.
- Do not create a new session.

### Delete Review

Implement:

```python
async def delete(
    self,
    session: AsyncSession,
    review_id: int,
) -> bool:
    ...
```

Requirements:

- Find the review by ID.
- Physically delete the review row.
- Return `True` when deleted.
- Return `False` when not found.

Unlike Film deletion, Review deletion is a real delete.

## 5. UserDAO

Create a typed asynchronous `UserDAO`.

Implement:

```python
async def get_by_email(
    self,
    session: AsyncSession,
    email: str,
) -> User | None:
    ...
```

Requirements:

- Search by email.
- Return User when found.
- Return `None` when not found.
- Use the supplied AsyncSession.
- Never create a session inside the DAO.

This will be used by authentication later.

## 6. AsyncSession Rules

Every DAO method MUST receive:

```python
session: AsyncSession
```

Correct:

```python
async def get_by_id(
    self,
    session: AsyncSession,
    film_id: int,
) -> Film | None:
```

Incorrect:

```python
async def get_by_id(self, film_id: int):
    session = AsyncSession(...)
```

Never create an engine, session factory, or AsyncSession inside DAO methods.

Use the session supplied by FastAPI dependency injection.

## 7. Service Layer

Create or update thin services.

Services must call DAOs and must not execute SQLAlchemy queries directly.

Example:

```python
async def get_film(
    session: AsyncSession,
    film_id: int,
) -> Film | None:
    return await film_dao.get_by_id(session, film_id)
```

Do not put `session.execute()` or other direct database operations in services.

For this exercise, keep services thin. The goal is to establish the architecture.

## 8. Handler Layer

Handlers must call services.

Example:

```python
async def get_film(
    film_id: int,
    session: AsyncSession,
):
    return await film_service.get_film(session, film_id)
```

Handlers must not call DAOs directly and must not execute database queries.

Correct:

```text
Handler → Service → DAO
```

Incorrect:

```text
Handler → DAO
```

## 9. Update At Least Two Routes

Update at least two existing route handlers. Reuse existing endpoints if equivalent routes already exist.

### Route 1 — Get Film

Use the existing film detail endpoint or create:

```text
GET /films/{film_id}
```

Required flow:

```text
Route
  ↓
Handler
  ↓
Film Service
  ↓
FilmDAO.get_by_id()
  ↓
AsyncSession
  ↓
PostgreSQL
```

The route must not call the DAO directly.

### Route 2 — List Reviews for Film

Use the existing review endpoint or create:

```text
GET /films/{film_id}/reviews
```

Required flow:

```text
Route
  ↓
Handler
  ↓
Review Service
  ↓
ReviewDAO.list_by_film()
  ↓
AsyncSession
  ↓
PostgreSQL
```

The route must not call the DAO directly.

## 10. Dependency Injection

Use the project's existing FastAPI database dependency.

The session should be supplied through the existing dependency, for example:

```python
Depends(get_session)
```

Do not create a new session manually inside DAOs.

The intended flow is:

```text
FastAPI
  ↓
get_session()
  ↓
AsyncSession
  ↓
Route
  ↓
Handler
  ↓
Service
  ↓
DAO
```

## 11. Error Handling

DAO methods should return explicit absent values where required.

Examples:

```text
Film | None
User | None
bool
```

The service layer can decide what application-level behavior should happen when a DAO returns `None`.

Do not put unnecessary business logic into the DAO.

## 12. Type Hints

All DAO methods must have complete type hints.

Use appropriate types such as:

```text
AsyncSession
Film
Review
User
FilmUpdate
Film | None
list[Film]
list[Review]
User | None
float | None
bool
```

Do not leave DAO methods untyped.

## 13. Code Quality

- Use async SQLAlchemy APIs.
- Use `await` for async database operations.
- Keep all direct database queries inside DAO classes.
- Keep handlers thin.
- Keep services thin.
- Use dependency injection for AsyncSession.
- Reuse existing models and schemas.
- Follow existing naming conventions.
- Do not add unnecessary dependencies.
- Do not rewrite unrelated working code.
- Keep the implementation simple and readable.

## 14. Verification

After implementation, inspect the final code and verify:

```text
Route       → does NOT execute database queries
Route       → does NOT call DAO directly

Handler     → does NOT execute database queries
Handler     → does NOT call DAO directly

Service     → does NOT execute database queries
Service     → calls DAO

DAO         → contains database queries
DAO         → receives AsyncSession
DAO         → does NOT create AsyncSession
```

The final architecture must be:

```text
HTTP Request
     ↓
   Route
     ↓
  Handler
     ↓
  Service
     ↓
    DAO
     ↓
AsyncSession
     ↓
PostgreSQL
```

## 15. Test Through `/docs`

Run the FastAPI application and open `/docs`.

Verify at least:

### Film

- Get existing film.
- Get non-existing film.
- List films.
- List films by genre.
- List films by year range.
- Create film.
- Update film.
- Soft delete film.

### Review

- List reviews for a film.
- Verify newest reviews appear first.
- Calculate average rating.
- Create review.
- Delete review.

### User

- Find existing user by email.
- Find unknown user by email.

## 16. Final Checklist

- [ ] FilmDAO exists.
- [ ] FilmDAO has `get_by_id`.
- [ ] Missing film returns `None`.
- [ ] FilmDAO has film listing.
- [ ] Genre filtering works.
- [ ] Year-range filtering works.
- [ ] FilmDAO has create.
- [ ] FilmDAO has update.
- [ ] FilmDAO has soft delete.
- [ ] Soft delete does not remove the row.
- [ ] Inactive films are excluded from normal listing.
- [ ] ReviewDAO exists.
- [ ] ReviewDAO lists reviews by film.
- [ ] Reviews are newest first.
- [ ] ReviewDAO calculates average rating.
- [ ] No reviews returns `None` for average rating.
- [ ] ReviewDAO creates reviews.
- [ ] ReviewDAO deletes reviews.
- [ ] UserDAO exists.
- [ ] UserDAO finds users by email.
- [ ] Every DAO method receives AsyncSession.
- [ ] No DAO creates its own session.
- [ ] Services call DAOs.
- [ ] Handlers call services.
- [ ] Routes call handlers.
- [ ] At least two routes use Route → Handler → Service → DAO.
- [ ] No direct database queries exist in routes.
- [ ] No direct database queries exist in handlers.
- [ ] No direct database queries exist in services.
- [ ] Application starts successfully.
- [ ] `/docs` works.

## Important Antigravity Instruction

First inspect the existing project and understand the current implementation.

Then implement this exercise using the existing architecture.

Do not generate isolated example files. Modify the actual project so the DAO layer works end-to-end.

After implementation:

1. Show which files were created.
2. Show which files were modified.
3. Explain briefly what each modified file does.
4. Check for import errors.
5. Run the project's configured type checker if available.
6. Start/check the FastAPI application if possible.
7. Verify the two required request flows follow:

```text
Route → Handler → Service → DAO
```

Do not stop after creating DAO classes. Wire the DAOs into the existing application.
