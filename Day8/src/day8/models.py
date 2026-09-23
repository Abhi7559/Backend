"""Data models for Day 8 Async Batch Job Processor."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generic, Optional, TypeVar


class JobPriority(str, Enum):
    """Job priority levels influencing processing duration."""
    HIGH = "HIGH"        # Fast path (~0.15s)
    MEDIUM = "MEDIUM"    # Standard path (~0.30s)
    LOW = "LOW"          # Heavy enrichment (~0.60s)


T = TypeVar("T")


@dataclass(frozen=True)
class Job(Generic[T]):
    """Represents an individual enrichment job unit."""
    id: str
    job_type: str
    priority: JobPriority
    payload: T


@dataclass
class JobResult:
    """The outcome of an individual processed job."""
    job_id: str
    success: bool
    duration: float
    result_data: Optional[Any] = None
    failure_reason: Optional[str] = None


@dataclass
class BatchSummary:
    """Consolidated report produced after all batch jobs finish."""
    total_jobs: int
    successful_count: int
    failed_count: int
    failure_breakdown: Dict[str, int] = field(default_factory=dict)
    total_wall_clock_time: float = 0.0
    theoretical_sequential_time: float = 0.0
    speedup_factor: float = 0.0
