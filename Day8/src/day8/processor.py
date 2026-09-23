"""
Day 8: Async Batch Job Processor (Entrypoint / Demo)
Runs nightly batch enrichment jobs concurrently and produces a structured summary.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List

try:
    from day8.models import Job, JobPriority
    from day8.supervisor import BatchSupervisor
except ImportError:
    from models import Job, JobPriority  # type: ignore
    from supervisor import BatchSupervisor  # type: ignore


def build_sample_jobs() -> List[Job[Dict[str, Any]]]:
    """Builds a realistic batch of nightly enrichment jobs."""
    return [
        Job("JOB-001", "UserDemographics", JobPriority.HIGH, {"user_id": 101}),
        Job("JOB-002", "ProductPricing", JobPriority.MEDIUM, {"sku": "A1"}),
        Job("JOB-003", "OrderHistory", JobPriority.LOW, {"account_id": 450}),
        Job("JOB-004", "UserCreditScore", JobPriority.HIGH, {"user_id": 102}),
        # Faulty payload that triggers a validation error
        Job("JOB-005", "InventorySync", JobPriority.HIGH, {"trigger_error": "Negative quantity detected"}),
        Job("JOB-006", "FraudAnalysis", JobPriority.MEDIUM, {"ip": "192.168.1.1"}),
        # Stalled job that exceeds the 1.0s timeout
        Job("JOB-007", "ExternalPartnerSync", JobPriority.HIGH, {"simulate_hang": True}),
        Job("JOB-008", "EmailReputation", JobPriority.LOW, {"domain": "example.com"}),
    ]


async def main() -> None:
    jobs = build_sample_jobs()
    supervisor = BatchSupervisor(max_concurrency=3, per_job_timeout=1.0)
    
    summary = await supervisor.run_batch(jobs)

    print("\n" + "=" * 75)
    print("                BATCH EXECUTION SUMMARY")
    print("=" * 75)
    print(f"Total Jobs Processed       : {summary.total_jobs}")
    print(f"Successful Jobs            : {summary.successful_count} [PASSED]")
    print(f"Failed Jobs                : {summary.failed_count} [FAILED]")
    
    if summary.failure_breakdown:
        print("\nFailure Breakdown:")
        for reason, count in summary.failure_breakdown.items():
            print(f"  - {reason}: {count} job(s)")

    print("\nPerformance Comparison:")
    print(f"  * Sequential Time (Sum)  : {summary.theoretical_sequential_time:.3f} seconds")
    print(f"  * Wall-Clock Time (Async): {summary.total_wall_clock_time:.3f} seconds")
    print(f"  * Speedup Factor         : {summary.speedup_factor:.2f}x faster!")
    print("=" * 75)


if __name__ == "__main__":
    # asyncio.run() creates the event loop, runs main(), and cleanly closes it
    asyncio.run(main())
