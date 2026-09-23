"""Supervisor module: Manages batch concurrency, timeouts, and streaming."""
from __future__ import annotations

import asyncio
import time
from typing import Any, AsyncGenerator, Dict, List

try:
    from day8.models import BatchSummary, Job, JobResult
    from day8.worker import process_single_job
except ImportError:
    from models import BatchSummary, Job, JobResult  # type: ignore
    from worker import process_single_job  # type: ignore


class BatchSupervisor:
    """
    Supervises concurrent job execution with:
    - Semaphore-based concurrency throttling (never runs all at once)
    - Per-job timeout protection (cancels hung jobs without stopping the batch)
    - Streaming results via async generators (async for)
    """

    def __init__(self, max_concurrency: int = 3, per_job_timeout: float = 1.0) -> None:
        self.max_concurrency = max_concurrency
        self.per_job_timeout = per_job_timeout
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def _process_with_guard(self, job: Job[Any]) -> JobResult:
        """
        Guards an individual job with:
        1. async with self._semaphore: Enforces maximum concurrent workers.
        2. asyncio.wait_for: Cancels job if it exceeds per_job_timeout.
        """
        # async with demonstrates the Async Context Manager Protocol
        async with self._semaphore:
            start = time.perf_counter()
            try:
                # Enforce per-job timeout
                result = await asyncio.wait_for(
                    process_single_job(job),
                    timeout=self.per_job_timeout,
                )
                return result
            except asyncio.TimeoutError:
                duration = time.perf_counter() - start
                return JobResult(
                    job_id=job.id,
                    success=False,
                    duration=duration,
                    failure_reason=f"TimeoutError: Exceeded {self.per_job_timeout:.1f}s threshold",
                )
            except Exception as exc:
                duration = time.perf_counter() - start
                return JobResult(
                    job_id=job.id,
                    success=False,
                    duration=duration,
                    failure_reason=f"UnexpectedError: {exc}",
                )

    async def stream_results(self, jobs: List[Job[Any]]) -> AsyncGenerator[JobResult, None]:
        """
        Demonstrates 'async for' & Async Generators.
        Streams completed results as tasks finish.
        """
        # Wrap each job into an asyncio.Task to run concurrently
        tasks = [
            asyncio.create_task(self._process_with_guard(job))
            for job in jobs
        ]
        
        # as_completed yields tasks as they complete
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            yield result

    async def run_batch(self, jobs: List[Job[Any]]) -> BatchSummary:
        """
        Executes all jobs with concurrency limit and generates a typed summary.
        Uses 'async for' to consume results from stream_results.
        """
        wall_start = time.perf_counter()
        results: List[JobResult] = []
        sequential_time_sum = 0.0

        print(f"[BATCH START] {len(jobs)} jobs | Max Concurrency: {self.max_concurrency} | Timeout: {self.per_job_timeout}s")
        print("-" * 75)

        # Consume the stream of results using 'async for'
        async for res in self.stream_results(jobs):
            results.append(res)
            sequential_time_sum += res.duration
            status = "[OK] SUCCESS" if res.success else f"[FAIL] FAILED ({res.failure_reason})"
            print(f"  [{res.job_id:<8}] {status:<45} | Took: {res.duration:.3f}s")

        wall_duration = time.perf_counter() - wall_start

        # Compute summary metrics
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        breakdown: Dict[str, int] = {}
        for f_res in failed:
            reason = f_res.failure_reason or "Unknown"
            breakdown[reason] = breakdown.get(reason, 0) + 1

        speedup = sequential_time_sum / wall_duration if wall_duration > 0 else 1.0

        return BatchSummary(
            total_jobs=len(jobs),
            successful_count=len(successful),
            failed_count=len(failed),
            failure_breakdown=breakdown,
            total_wall_clock_time=wall_duration,
            theoretical_sequential_time=sequential_time_sum,
            speedup_factor=speedup,
        )
