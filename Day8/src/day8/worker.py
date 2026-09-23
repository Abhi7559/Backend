"""Worker module: Asynchronously processes individual jobs."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict

try:
    from day8.models import Job, JobPriority, JobResult
except ImportError:
    from models import Job, JobPriority, JobResult  # type: ignore

# Duration mapping based on priority (simulating real I/O workloads)
PRIORITY_DURATIONS: Dict[JobPriority, float] = {
    JobPriority.HIGH: 0.15,
    JobPriority.MEDIUM: 0.30,
    JobPriority.LOW: 0.60,
}


async def process_single_job(job: Job[Any]) -> JobResult:
    """
    Asynchronously processes a single job.
    
    Demonstrates:
    - async def / await: Suspends via asyncio.sleep without blocking the thread.
    - Error simulation for faulty payloads.
    - Hang simulation to test timeout handling.
    """
    start = time.perf_counter()
    
    # Base processing delay derived from priority
    base_duration = PRIORITY_DURATIONS.get(job.priority, 0.30)
    
    # Check for test triggers in payload
    if isinstance(job.payload, dict):
        # 1. Simulate an intentional error
        if job.payload.get("trigger_error"):
            await asyncio.sleep(0.05)
            duration = time.perf_counter() - start
            return JobResult(
                job_id=job.id,
                success=False,
                duration=duration,
                failure_reason=f"DataValidationError: {job.payload.get('trigger_error')}",
            )
        
        # 2. Simulate a hung/slow network request to trigger timeouts
        if job.payload.get("simulate_hang"):
            base_duration = 5.0  # Far exceeds default timeout threshold

    # Non-blocking async sleep: yields control back to the event loop!
    await asyncio.sleep(base_duration)
    duration = time.perf_counter() - start

    # Return successful result
    return JobResult(
        job_id=job.id,
        success=True,
        duration=duration,
        result_data={
            "enriched": True,
            "job_type": job.job_type,
            "priority": job.priority.value,
        },
    )
