"""
Exercise: Generic Pipeline Utilities - Part 1
A clean, easy-to-understand code explaining Advanced Typing in Python.
All concepts in a single file!
"""
from __future__ import annotations

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
    overload,
)

# 1. Final -> Value cannot be changed/reassigned
PIPELINE_VERSION: Final[str] = "v1.0.0"



# 2. Literal & TypedDict & Annotated -> Define fixed options & Dict Shapes
# Literal restricts mode to only 3 specific strings
ModeType = Literal["strict", "permissive", "dry-run"]

# TypedDict defines the exact keys & types required for config
class PipelineConfig(TypedDict):
    name: Annotated[str, "Pipeline display name"]  # Annotated adds extra metadata
    mode: ModeType
    max_retries: int



# 3. Protocol -> Duck typing with type-checker support (No inheritance needed)
class ValidatorProtocol(Protocol):
    """Any object with a validate(item) -> bool method matches this Protocol."""
    def validate(self, item: int) -> bool:
        ...

# 4. TypeVar & Generic Class -> Type-Safe Container
T = TypeVar("T")  # Input element type
U = TypeVar("U")  # Output element type (after transform)
K = TypeVar("K")  # Key type (for group_by)

class DataPipeline(Generic[T]):
    """Container wrapping a list of items of any type T."""
    def __init__(self, items: Sequence[T]) -> None:
        self.items: List[T] = list(items)

    def filter(self, predicate: Callable[[T], bool]) -> DataPipeline[T]:
        """Filter items matching predicate, keeping type T."""
        return DataPipeline([x for x in self.items if predicate(x)])

    def transform(self, mapper: Callable[[T], U]) -> DataPipeline[U]:
        """Transform each item from type T to new type U."""
        return DataPipeline([mapper(x) for x in self.items])

    def group_by(self, key_selector: Callable[[T], K]) -> Dict[K, List[T]]:
        """Group items into a dict using a key selector function."""
        result: Dict[K, List[T]] = {}
        for item in self.items:
            key = key_selector(item)
            result.setdefault(key, []).append(item)
        return result

    def get_items(self) -> List[T]:
        return self.items



# 5. Overload & Generic Function -> Function accepting Protocol or Callable
ItemT = TypeVar("ItemT")

# Overload signature 1: Accepting a Protocol validator object
@overload
def filter_records(items: Sequence[ItemT], validator: ValidatorProtocol) -> List[ItemT]:
    ...

# Overload signature 2: Accepting a plain function predicate
@overload
def filter_records(items: Sequence[ItemT], validator: Callable[[ItemT], bool]) -> List[ItemT]:
    ...

# Actual implementation
def filter_records(items: Sequence[ItemT], validator: any) -> List[ItemT]:
    """Filters records using either a Validator object or a function."""
    valid_items: List[ItemT] = []
    for item in items:
        # Check if validator object has a .validate() method or is callable
        if hasattr(validator, "validate"):
            if validator.validate(item):
                valid_items.append(item)
        elif callable(validator):
            if validator(item):
                valid_items.append(item)
    return valid_items


# 6. Runnable Demo Code
class PositiveNumberValidator:
    """Matches ValidatorProtocol automatically WITHOUT inheriting from it!"""
    def validate(self, item: int) -> bool:
        return item > 0


def main() -> None:
    print(f"=== Pipeline Version: {PIPELINE_VERSION} ===")

    # A. Demo TypedDict & Literal
    config: PipelineConfig = {
        "name": "User Sync Pipeline",
        "mode": "strict",
        "max_retries": 3,
    }
    print(f"\n1. Config Payload: {config}")

    # B. Demo Generic DataPipeline
    numbers = (10, -5, 20, -15, 30)
    pipeline = DataPipeline(numbers)

    # Chain operations: Filter positive numbers -> Transform int to string formatted text
    processed = (
        pipeline
        .filter(lambda x: x > 0)             # DataPipeline[int]
        .transform(lambda x: f"Num: {x}")    # DataPipeline[str]
    )
    print(f"\n2. Processed Pipeline Items: {processed.get_items()}")

    # Grouping Demo
    words = ["apple", "banana", "apricot", "cherry", "blueberry"]
    grouped = DataPipeline(words).group_by(lambda w: w[0])
    print(f"\n3. Grouped Words: {grouped}")

    # C. Demo Protocol & Overload Function
    raw_nums = [-10, 15, -2, 42, 0]
    
    # Passing a custom class matching Protocol shape
    positive_only = filter_records(raw_nums, PositiveNumberValidator())
    print(f"\n4. Filtered using Protocol Validator: {positive_only}")

    # Passing a plain lambda function (uses second @overload signature)
    even_only = filter_records(raw_nums, lambda x: x % 2 == 0)
    print(f"5. Filtered using Lambda Function: {sorted(even_only)}")


if __name__ == "__main__":
    main()
