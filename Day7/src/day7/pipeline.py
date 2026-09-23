"""
Exercise: Generic Pipeline Utilities - Part 2 (Behavioural Decorators)
Combines Day 6 (Part 1) Type-Safe Pipeline with Day 7 (Part 2) Decorators:
1. time_it: Measures and prints execution time (preserves metadata via @wraps)
2. retry: Retries failing function with increasing backoff delay
3. cache_with_ttl: Caches return value for a configurable duration (TTL in seconds)
All 3 decorators are fully stackable!
"""
from __future__ import annotations

import time
from functools import wraps
from typing import (
    TypeVar,
    Generic,
    Protocol,
    Literal,
    TypedDict,
    Final,
    Annotated,
    Callable,
    Sequence,
    List,
    Dict,
    Any,
    overload,
)


# PART 2: BEHAVIOURAL DECORATORS


# 1. Timing Decorator (Basic Decorator with @wraps)
def time_it(func: Callable) -> Callable:
    """Measures execution time, preserving func name, docstring, and annotations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[time_it] '{func.__name__}' took {duration:.6f} seconds")
        return result
    return wrapper


# 2. Retry with Backoff Decorator (Decorator accepting its own arguments)
def retry(max_attempts: int = 3, base_delay: float = 0.1, fatal_errors: tuple = (ValueError,)):
    """
    Retries function up to max_attempts with increasing delay.
    Stops immediately if error is in fatal_errors.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except fatal_errors as fatal:
                    print(f"[retry] Fatal error '{fatal}'! Aborting retries immediately.")
                    raise
                except Exception as err:
                    print(f"[retry] Attempt {attempt}/{max_attempts} failed: {err}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
                    delay *= 2  # Increasing backoff
        return wrapper
    return decorator


# 3. Cache with TTL Decorator (In-memory caching with expiration)
def cache_with_ttl(ttl_seconds: float = 2.0):
    """Caches return value for ttl_seconds based on identical arguments."""
    def decorator(func: Callable) -> Callable:
        cache_store: Dict[tuple, tuple[Any, float]] = {}  # key -> (result, timestamp)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a simple hashable cache key from args
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            if key in cache_store:
                cached_val, cached_time = cache_store[key]
                if now - cached_time < ttl_seconds:
                    print(f"[cache] Returning cached result for '{func.__name__}'")
                    return cached_val

            result = func(*args, **kwargs)
            cache_store[key] = (result, now)
            return result
        return wrapper
    return decorator



# PART 1: CORE DATA PIPELINE UTILITIES (From Day 6)


PIPELINE_VERSION: Final[str] = "v2.0.0"

ModeType = Literal["strict", "permissive", "dry-run"]

class PipelineConfig(TypedDict):
    name: Annotated[str, "Pipeline display name"]
    mode: ModeType
    max_retries: int

class ValidatorProtocol(Protocol):
    def validate(self, item: int) -> bool:
        ...

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")

class DataPipeline(Generic[T]):
    def __init__(self, items: Sequence[T]) -> None:
        self.items: List[T] = list(items)

    def filter(self, predicate: Callable[[T], bool]) -> DataPipeline[T]:
        return DataPipeline([x for x in self.items if predicate(x)])

    def transform(self, mapper: Callable[[T], U]) -> DataPipeline[U]:
        return DataPipeline([mapper(x) for x in self.items])

    def group_by(self, key_selector: Callable[[T], K]) -> Dict[K, List[T]]:
        result: Dict[K, List[T]] = {}
        for item in self.items:
            key = key_selector(item)
            result.setdefault(key, []).append(item)
        return result

    def get_items(self) -> List[T]:
        return self.items


ItemT = TypeVar("ItemT")

@overload
def filter_records(items: Sequence[ItemT], validator: ValidatorProtocol) -> List[ItemT]:
    ...

@overload
def filter_records(items: Sequence[ItemT], validator: Callable[[ItemT], bool]) -> List[ItemT]:
    ...

def filter_records(items: Sequence[ItemT], validator: any) -> List[ItemT]:
    valid_items: List[ItemT] = []
    for item in items:
        if hasattr(validator, "validate"):
            if validator.validate(item):
                valid_items.append(item)
        elif callable(validator):
            if validator(item):
                valid_items.append(item)
    return valid_items


# DEMO: COMBINING PART 1 + PART 2 WITH STACKED DECORATORS


class PositiveNumberValidator:
    def validate(self, item: int) -> bool:
        return item > 0


# Flaky external step simulator for testing retry
attempt_counter = 0

@retry(max_attempts=3, base_delay=0.05, fatal_errors=(ValueError,))
def fetch_remote_multiplier() -> int:
    """Fails twice, then succeeds on 3rd attempt."""
    global attempt_counter
    attempt_counter += 1
    if attempt_counter < 3:
        raise ConnectionError(f"Temporary network error on try {attempt_counter}")
    return 10


# Demonstrating STACKED decorators:
# Bottom-up execution: cache_with_ttl -> time_it
@time_it
@cache_with_ttl(ttl_seconds=1.0)
def process_pipeline_data(multiplier: int, label: str) -> List[str]:
    """Pipeline processing function protected with stacked decorators."""
    nums = (10, -5, 20, -15, 30)
    pipeline = DataPipeline(nums)
    
    # Process pipeline using Part 1 abstractions
    result = (
        pipeline
        .filter(lambda x: x > 0)
        .transform(lambda x: f"{label}: {x * multiplier}")
    )
    return result.get_items()


def main() -> None:
    print(f"=== Pipeline Version: {PIPELINE_VERSION} ===")

    # 1. Test Retry with Backoff
    print("\n--- 1. Testing @retry ---")
    multiplier = fetch_remote_multiplier()
    print(f"Fetched multiplier: {multiplier}")

    # 2. Test Stacked Decorators (@time_it + @cache_with_ttl)
    print("\n--- 2. Testing Stacked Decorators (First Call - Computes) ---")
    output1 = process_pipeline_data(multiplier, "Score")
    print("Output:", output1)

    print("\n--- 3. Testing Cache Hit (Second Call with identical arguments) ---")
    output2 = process_pipeline_data(multiplier, "Score")
    print("Output:", output2)

    # Verify metadata preservation via @wraps
    print("\n--- 4. Metadata preserved by @wraps ---")
    print(f"Function name: {process_pipeline_data.__name__}")
    print(f"Docstring:     {process_pipeline_data.__doc__}")


if __name__ == "__main__":
    main()
