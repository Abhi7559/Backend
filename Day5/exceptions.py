
"""Custom exceptions for the Library Catalogue domain."""


class LibraryError(Exception):
    """Base exception class for all library errors."""
    pass


class ResourceNotFoundError(LibraryError):
    """Raised when a requested resource (Book or Member) is not found."""
    def __init__(self, resource_type: str, resource_id: str) -> None:
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{self.resource_type} with ID '{self.resource_id}' was not found.")


class BusinessRuleError(LibraryError):
    """Raised when a business rule is violated (e.g. loan limit exceeded)."""
    def __init__(self, rule_name: str, message: str) -> None:
        self.rule_name = rule_name
        self.message = message
        super().__init__(f"[{self.rule_name}] {self.message}")


class InvalidInputError(LibraryError):
    """Raised when invalid input parameters are provided."""
    def __init__(self, field_name: str, message: str) -> None:
        self.field_name = field_name
        self.message = message
        super().__init__(f"Invalid value for '{self.field_name}': {self.message}")
