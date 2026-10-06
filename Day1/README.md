# Day 1 - Film Review Platform API

FastAPI application for the Film Review Platform API with structured routing, services, and DAOs.

## Requirements
- Python >= 3.12
- `uv` (recommended) or `pip`

## Running the Application

Using `uv`:
```bash
uv run uvicorn main:app --reload
```

Or using python virtual environment:
```bash
python -m venv .venv
# Activate virtual environment
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e .
uvicorn main:app --reload
```

## API Endpoints
- Health Check: `GET /health`
- Swagger UI Documentation: `GET /docs`
- ReDoc Documentation: `GET /redoc`
- Films API: `/api/v1/films`
- Reviews API: `/api/v1/reviews`
- Users API: `/api/v1/users`
