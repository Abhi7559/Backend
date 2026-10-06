import uuid
from typing import Annotated
from fastapi import Header


def get_trace_id(
    x_trace_id: Annotated[str | None, Header(description="Optional request trace identifier")] = None,
) -> str:
    """
    Reusable dependency extracting X-Trace-ID header.
    If missing or empty, generates a new UUID4.
    """
    if x_trace_id and x_trace_id.strip():
        return x_trace_id.strip()
    return str(uuid.uuid4())
