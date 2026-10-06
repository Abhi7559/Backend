# FastAPI Dependency Injection & Configuration

## Exercise: Film Review Platform — Configuration & Shared Dependencies

### Objective

Implement a centralized configuration system and reusable dependency injection system for the Film Review Platform using FastAPI.

The implementation must demonstrate:

* Dependency Injection using `Depends()`.
* Reusable dependency functions.
* Dependency chains and dependency resolution.
* Shared resources across requests.
* Centralized configuration using a `.env` file.
* Typed configuration using Pydantic Settings.
* A single configuration object instantiated at import time.
* Fail-fast validation when required configuration is missing.
* Database session and request trace ID dependencies.
* OpenAPI documentation for dependency-related request parameters.

**Important:** Implement the exercise using simple, beginner-friendly Python code. Do not introduce unnecessary abstractions or complex patterns.

---

## 1. Project Structure

Follow the existing project structure if one is already present.

Otherwise, use the following structure:

```text
film-review-platform/
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
│
└── app/
    ├── __init__.py
    ├── main.py
    │
    ├── core/
    │   ├── __init__.py
    │   └── config.py
    │
    ├── dependencies/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── trace.py
    │   └── auth.py
    │
    └── routes/
        ├── __init__.py
        └── films.py
```

Do not create a test folder or use pytest.

---

## 2. Centralized Configuration

Create a dedicated configuration module:

`app/core/config.py`

### Requirements

1. Use Pydantic Settings to define a typed `Settings` class.

2. Load all configuration values from the `.env` file.

3. Define the following settings:

   * `DATABASE_URL`: Database connection URL.
   * `TOKEN_SECRET_KEY`: Secret key used for token signing.
   * `TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiry duration.
   * `TOKEN_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiry duration.
   * `CORS_ORIGINS`: List of allowed frontend origins.
   * `API_VERSION`: API version string.

4. Use appropriate Python types for all settings.

5. Create exactly one shared configuration object named `settings`.

6. Instantiate the configuration object once at module import time.

7. Do not reload the `.env` file in other modules.

8. Do not use `os.getenv()` or `os.environ` outside the configuration module.

9. Ensure missing required configuration values raise a descriptive validation error during application startup.

10. Use a clear configuration error message that identifies the missing setting.

### Expected behavior

When the application starts:

* All required settings are loaded.
* Values are validated.
* The shared configuration object is created.
* The application fails to start if required settings are missing or invalid.

---

## 3. Environment Variables

Create a `.env.example` file containing placeholder values for all required settings.

Example:

```dotenv
DATABASE_URL=postgresql+asyncpg://user:password@localhost/film_review
TOKEN_SECRET_KEY=replace-with-a-secure-secret
TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES=30
TOKEN_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
API_VERSION=v1
```

Requirements:

* Create a local `.env` file for development if needed.
* Add `.env` to `.gitignore`.
* Never commit real secrets.
* Keep `.env.example` free of real credentials.
* Ensure the application can load the configuration from the project root.

---

## 4. Configuration Dependency

Create:

`app/dependencies/config.py`

### Requirements

1. Import the shared `settings` object from `app/core/config.py`.
2. Create a reusable dependency function named `get_config()`.
3. Return the shared configuration object.
4. Add an appropriate return type.
5. Do not instantiate a new configuration object inside the dependency.

### Expected dependency usage

Routes must obtain configuration through `Depends(get_config)` rather than importing the configuration object directly into route handlers.

---

## 5. Database Session Dependency

Create:

`app/dependencies/database.py`

### Requirements

1. Create a reusable dependency function named `get_db()`.
2. Use `yield` to provide a placeholder database session.
3. Include a `try/finally` structure for the future cleanup logic.
4. Keep the dependency structured so a real asynchronous database session can replace the placeholder later.
5. Do not connect to a real database in this exercise.
6. Do not change route function signatures when the real database session is integrated later.

### Expected behavior

The dependency should provide a placeholder value to routes.

The placeholder must be clearly identified as a temporary value and must not pretend to be a working database session.

---

## 6. Request Trace ID Dependency

Create:

`app/dependencies/trace.py`

### Requirements

1. Create a dependency function named `get_trace_id()`.
2. Read the trace identifier from the `X-Trace-ID` request header.
3. If the header is present, return its value.
4. If the header is missing or empty, generate a fresh UUID.
5. Return the trace identifier as a string.
6. Use FastAPI's `Header` parameter to extract the header.
7. Make the dependency reusable across different route handlers.

### Expected behavior

Request with a trace ID:

```http
GET /films/
X-Trace-ID: trace-12345
```

The dependency returns:

```text
trace-12345
```

Request without a trace ID:

```http
GET /films/
```

The dependency generates and returns a new UUID.

---

## 7. Reusable Dependency Functions

Demonstrate how FastAPI's `Depends()` mechanism injects dependency results into route handlers.

### Requirements

Create and use these dependencies:

| Dependency       | Function         |
| ---------------- | ---------------- |
| Configuration    | `get_config()`   |
| Database session | `get_db()`       |
| Request trace ID | `get_trace_id()` |

Each dependency must:

* Be reusable.
* Have appropriate type annotations.
* Be independent of route-specific business logic.
* Be declared using `Depends()` wherever needed.

---

## 8. Dependency Chains

Demonstrate a dependency chain in the application.

### Requirements

1. Create a reusable dependency named `get_current_user()`.
2. Make `get_current_user()` depend on `get_config()` using `Depends()`.
3. Use the configuration dependency to access the token secret key.
4. Keep authentication logic simple and suitable for the current exercise.
5. Do not implement a complete JWT authentication system.
6. Use a placeholder current-user result if necessary.
7. Demonstrate how FastAPI resolves the nested dependency tree.

### Expected dependency flow

```text
Route Handler
      |
      v
get_current_user()
      |
      v
get_config()
      |
      v
Shared Settings Object
```

The route should receive the result of `get_current_user()` without manually calling the dependency function.

---

## 9. Current User Dependency

Create:

`app/dependencies/auth.py`

### Requirements

1. Create a dependency function named `get_current_user()`.
2. Declare `config: Settings = Depends(get_config)`.
3. Use the injected configuration object.
4. Return a simple placeholder user object or dictionary.
5. Include appropriate type annotations.
6. Keep the implementation beginner-friendly.
7. Do not add database authentication or JWT validation.

The purpose is to demonstrate dependency chaining, not to build a complete authentication system.

---

## 10. Apply Dependencies to Routes

Update:

`app/routes/films.py`

Create or update the following routes:

### Route 1: Retrieve all films

```http
GET /films/
```

### Route 2: Retrieve a film by ID

```http
GET /films/{film_id}
```

### Requirements

Both routes must declare all three shared dependencies:

* `get_config()`
* `get_db()`
* `get_trace_id()`

At least one route must also declare the current-user dependency to demonstrate dependency chaining.

Use `Depends()` for all dependency declarations.

### Route response

Return a meaningful JSON response containing:

* A descriptive message.
* API version.
* Trace ID.
* Placeholder database information.
* Current-user information where applicable.

Do not expose the token secret key in any API response.

Use simple and meaningful response messages.

---

## 11. Dependency Sharing and Caching

Demonstrate how FastAPI shares dependency results within a single request.

### Requirements

1. Use the same dependency function wherever a shared resource is needed.
2. Explain how FastAPI's default dependency caching works.
3. Avoid creating duplicate configuration objects.
4. Ensure the shared configuration object is reused.
5. Keep the database session dependency reusable.
6. Do not disable dependency caching unless necessary.

The implementation should make it clear that Python module caching and FastAPI dependency caching are separate mechanisms.

---

## 12. FastAPI Application Setup

Update:

`app/main.py`

### Requirements

1. Create the FastAPI application.
2. Register the film router.
3. Use the centralized configuration object to access the API version.
4. Ensure configuration validation happens before the application starts serving requests.
5. Keep the application setup simple.

Use a meaningful application title.

---

## 13. OpenAPI Documentation

Verify that FastAPI correctly generates the API documentation.

### Requirements

1. Ensure both film routes appear in Swagger UI.
2. Ensure the `X-Trace-ID` header is documented as an optional request header.
3. Ensure internal dependencies such as configuration and database sessions are not exposed as ordinary request parameters.
4. Ensure the route parameters and response schemas are correctly documented.
5. Verify the generated OpenAPI schema.

### Documentation endpoints

```text
/docs
/openapi.json
```

---

## 14. Error Handling and Fail-Fast Validation

### Requirements

1. Required configuration values must not silently default to empty strings.
2. Missing configuration must raise a clear validation error.
3. Invalid configuration types must produce meaningful validation errors.
4. Configuration must be validated before the application handles requests.
5. Do not catch configuration errors and silently continue with invalid settings.
6. Do not print or expose secret values in error messages.

---

## 15. Code Quality Requirements

* Use beginner-friendly Python code.
* Use meaningful function and variable names.
* Add type annotations to dependency functions.
* Keep configuration, dependencies, and routes in separate modules.
* Avoid unnecessary abstractions.
* Do not use global mutable state for request-specific data.
* Do not use `os.getenv()` or `os.environ` outside `app/core/config.py`.
* Do not create a new configuration object inside route handlers.
* Do not create a real database connection.
* Do not implement full authentication.
* Do not create a test folder.
* Do not install pytest.
* Preserve existing project functionality wherever possible.

---

## 16. Execution Instructions

The application must run using:

```powershell
uv run uvicorn app.main:app --reload
```

The API documentation must be accessible at:

```text
http://127.0.0.1:8000/docs
```

---

## 17. Final Verification Checklist

Before completing the exercise, verify the following:

* [ ] A typed `Settings` class exists.
* [ ] All required environment settings are loaded from `.env`.
* [ ] A single shared `settings` object is created at import time.
* [ ] No environment variable reads exist outside the configuration module.
* [ ] Missing required settings cause a startup validation error.
* [ ] `get_config()` provides the shared configuration object.
* [ ] `get_db()` yields a placeholder database session.
* [ ] `get_trace_id()` extracts the header or generates a UUID.
* [ ] `get_current_user()` demonstrates a dependency chain.
* [ ] At least two route handlers use all three shared dependencies.
* [ ] At least one route demonstrates the current-user dependency.
* [ ] FastAPI dependency caching is used appropriately.
* [ ] Configuration secrets are never exposed in API responses.
* [ ] OpenAPI documents the trace ID header correctly.
* [ ] The application starts successfully with valid configuration.
* [ ] The application fails clearly when required configuration is missing.
* [ ] No test folder or pytest dependency is added.

---

## 18. Completion Report

After implementation, provide a concise summary containing:

1. Files created or modified.
2. Dependencies implemented.
3. How dependency chaining works in the project.
4. How configuration is loaded and validated.
5. How the trace ID is generated and injected.
6. How the database placeholder can be replaced later.
7. Commands used to run the application.
8. Verification results for Swagger UI and configuration validation.
9. Any remaining issues or incomplete requirements.

**Final instruction:** Implement the complete exercise in the existing project. Inspect the current codebase before making changes, preserve existing functionality, and ensure the implementation is simple, typed, and consistent with the requirements above.
