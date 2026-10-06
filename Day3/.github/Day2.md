# Film Review Platform — Pydantic v2 Schemas & Validation

## 1. Project Overview

Build a beginner-friendly Film Review Platform API using **FastAPI and Pydantic v2**.

The main goal is to create request and response schemas that validate incoming data and control the data returned by the API.

The existing routing skeleton is already in place. Read the existing project files before making changes.

**Important:** Use hardcoded data for now. Do not implement database connections.

## 2. Main Objectives

Implement the following features:

* Create request and response schemas for Film.
* Create request and response schemas for Review.
* Create a response schema for User that never exposes the password.
* Enable strict validation on all schemas.
* Add computed fields using Pydantic v2.
* Validate relationships between fields using model validators.
* Update at least two existing endpoints to use typed request and response schemas.
* Keep the code simple and beginner-friendly.

## 3. Technology Stack

Use the following technologies:

* Python
* FastAPI
* Pydantic v2
* Uvicorn
* uv for dependency management

Do not introduce unnecessary libraries.

## 4. Project Structure

First, inspect the existing project structure.

Keep the existing routing skeleton and extend it.

Use the following structure if the project does not already have an appropriate organization:

```text
film-review-platform/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── film.py
│   │   ├── review.py
│   │   └── user.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── films.py
│       └── reviews.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

Do not create unnecessary folders or files.

## 5. Film Schemas

Create the following schemas in `app/schemas/film.py`.

### 5.1 FilmCreate

This schema represents the data required to create a film.

Fields:

* `title`: string, required.
* `release_year`: integer, required.
* `genre`: string, required.
* `director`: string, required.

Validation requirements:

* All fields must be required.
* Reject strings when an integer is expected.
* Do not silently convert invalid data.
* Use strict mode.
* Reject empty or whitespace-only titles, genres, and director names.

### 5.2 FilmResponse

This schema represents the film data returned by the API.

Fields:

* `id`: integer, auto-generated for the hardcoded example.
* `title`: string.
* `release_year`: integer.
* `genre`: string.
* `director`: string.
* `years_ago`: computed integer field.

Requirements:

* Use Pydantic v2 `@computed_field` and `@property`.
* Calculate `years_ago` using the current year minus the release year.
* Do not require the client to provide `id` or `years_ago`.
* Enable strict mode.

## 6. Review Schemas

Create the following schemas in `app/schemas/review.py`.

### 6.1 ReviewCreate

This schema represents the data required to submit a review.

Fields:

* `film_id`: integer, required.
* `rating`: integer, required.
* `body`: string, required.

Validation requirements:

* `film_id` must be a strict integer.
* `rating` must be a strict integer between 1 and 10, inclusive.
* Reject floating-point values and numeric strings for the rating.
* `body` must contain at least 50 characters.
* Enable strict mode.
* Reject missing required fields.

### 6.2 ReviewResponse

This schema represents the review data returned by the API.

Fields:

* `id`: integer.
* `film_id`: integer.
* `rating`: integer.
* `body`: string.
* `reviewer_name`: string.
* `submitted_at`: datetime.

Requirements:

* The API should generate the review ID.
* Include the reviewer's display name.
* Include the submission timestamp.
* Use a valid Python `datetime` value for the timestamp.
* Enable strict mode.

## 7. User Response Schema

Create the following schema in `app/schemas/user.py`.

### UserResponse

Fields:

* `username`: string.
* `email`: valid email address.
* `role`: string.

Requirements:

* Enable strict mode.
* Never include the password in the response.
* Do not define a password field in the response schema.
* If the underlying user record contains a password, it must not appear in the serialized response.
* Use Pydantic's response serialization to expose only the allowed fields.

## 8. Field Relationship Validation

Implement at least one schema that validates a relationship between two of its own fields.

Create an additional schema named `ReleaseWindow` in `app/schemas/film.py`.

Fields:

* `start_year`: integer.
* `end_year`: integer.

Validation:

* `start_year` must be less than or equal to `end_year`.
* Use Pydantic v2 `@model_validator(mode="after")`.
* Raise a clear validation error when the start year is greater than the end year.
* Enable strict mode.

## 9. Strict Mode

All schemas must use Pydantic v2 strict mode.

Use:

```python
model_config = ConfigDict(strict=True)
```

Requirements:

* Apply strict mode to every schema.
* Do not allow automatic type conversion.
* An integer field must reject a string such as `"2024"`.
* An integer field must reject a float such as `2024.0`.
* A string field must reject non-string values.

## 10. API Endpoints

Update at least two existing endpoints from Day 1.

Use the existing routing skeleton whenever possible.

### Endpoint 1: Create Film

**Method:** POST

**Path:** `/films`

Request body:

```json
{
  "title": "Inception",
  "release_year": 2010,
  "genre": "Sci-Fi",
  "director": "Christopher Nolan"
}
```

Requirements:

* Accept a `FilmCreate` request body.
* Return a `FilmResponse`.
* Use a hardcoded ID such as `1`.
* Calculate `years_ago` automatically.
* Do not use a database.

Example response:

```json
{
  "id": 1,
  "title": "Inception",
  "release_year": 2010,
  "genre": "Sci-Fi",
  "director": "Christopher Nolan",
  "years_ago": 16
}
```

The computed value should reflect the current year.

### Endpoint 2: Create Review

**Method:** POST

**Path:** `/reviews`

Request body:

```json
{
  "film_id": 1,
  "rating": 9,
  "body": "This film has an excellent story, amazing visuals, and outstanding performances."
}
```

Requirements:

* Accept a `ReviewCreate` request body.
* Return a `ReviewResponse`.
* Use hardcoded data.
* Generate a review ID such as `1`.
* Include a reviewer display name such as `"Abhishek"`.
* Generate the submission timestamp using `datetime.now()`.
* Do not use a database.

### Optional Endpoint: Get User

**Method:** GET

**Path:** `/users/me`

Requirements:

* Return a `UserResponse`.
* Use hardcoded user data.
* Include a password in the internal example data to demonstrate that the response schema excludes it.
* Ensure the password is never returned.

## 11. Error Handling

FastAPI should automatically return validation errors for invalid request bodies.

Examples of invalid requests:

### Invalid Film

```json
{
  "title": "Inception",
  "release_year": "2010",
  "genre": "Sci-Fi",
  "director": "Christopher Nolan"
}
```

Expected behavior:

* Reject the request because `release_year` is a string instead of an integer.

### Invalid Review Rating

```json
{
  "film_id": 1,
  "rating": 11,
  "body": "This film has an excellent story, amazing visuals, and outstanding performances."
}
```

Expected behavior:

* Reject the request because the rating exceeds 10.

### Invalid Review Body

```json
{
  "film_id": 1,
  "rating": 9,
  "body": "Good movie"
}
```

Expected behavior:

* Reject the request because the body contains fewer than 50 characters.

## 12. Code Quality Requirements

* Write simple and readable Python code.
* Use meaningful variable and function names.
* Use type hints wherever appropriate.
* Follow Pydantic v2 conventions.
* Use `@computed_field` for computed values.
* Use `@model_validator` for field relationship validation.
* Keep schemas separate from route handlers.
* Avoid unnecessary abstractions.
* Do not add database logic.
* Do not add a test folder or pytest.
* Do not modify unrelated files.

## 13. Running the Project

Use the existing uv environment.

If dependencies are missing, install the required packages using uv.

Run the application with the appropriate existing entry point.

For example:

```bash
uv run uvicorn app.main:app --reload
```

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the endpoints and observe request validation and response schemas.

## 14. Expected Learning Outcomes

After completing this exercise, I should understand:

1. How to create request and response schemas using Pydantic v2.
2. How strict mode prevents automatic type conversion.
3. How to validate integer ranges and string lengths.
4. How to use `@computed_field` and `@property`.
5. How to validate relationships between fields using `@model_validator`.
6. How to prevent sensitive data such as passwords from appearing in API responses.
7. How to use `response_model` in FastAPI.
8. How FastAPI validates request bodies automatically.
9. How Pydantic schemas improve API documentation.
10. How to return hardcoded data using typed schemas without a database.

## 15. Final Instructions for Implementation

Before writing code:

1. Read the existing project files.
2. Identify the existing Day 1 routes and application entry point.
3. Reuse the existing structure and dependencies where possible.
4. Implement the schemas and update at least two existing endpoints.
5. Ensure all schemas use strict mode.
6. Keep the code simple and beginner-friendly.
7. Do not create a test folder or use pytest.
8. After implementation, explain which files were created or modified and how to run the project.
9. Provide sample requests and responses for the implemented endpoints.
