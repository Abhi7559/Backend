from collections.abc import Generator
from typing import Any


def get_db() -> Generator[dict[str, Any], None, None]:
    """
    Reusable dependency function yielding a placeholder database session.
    Structured with try/finally so real async db session cleanup can replace it later.
    """
    session = {
        "status": "connected",
        "type": "placeholder_session",
        "description": "Temporary placeholder session for Day 3 exercise",
    }
    try:
        yield session
    finally:
        # Cleanup logic will go here when connected to real database
        pass
