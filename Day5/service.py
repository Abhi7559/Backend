"""Business logic and Context Manager for Library operations."""

from typing import Any
from Day5.models import Book, Member, PremiumMember, Loan
from Day5.exceptions import ResourceNotFoundError, BusinessRuleError, InvalidInputError


# Sample Seed Data
BOOKS: list[Book] = [
    Book("978-0141439518", "Pride and Prejudice", "Jane Austen", 1813),
    Book("978-0451524935", "1984", "George Orwell", 1949),
    Book("978-0061120084", "To Kill a Mockingbird", "Harper Lee", 1960),
]

MEMBERS: list[Member] = [
    Member("M001", "Alice", max_loans=1),  # Limit set to 1 to easily trigger BusinessRuleError
    PremiumMember("M003", "Charlie", max_loans=10),
]

LOANS: list[Loan] = [
    Loan(member=MEMBERS[0], book=BOOKS[0], due_date="2026-09-20", returned=False),
]


def find_book(isbn: str) -> Book:
    """Find a book by ISBN or raise ResourceNotFoundError."""
    if not isbn or not isinstance(isbn, str):
        raise InvalidInputError("isbn", "ISBN must be a non-empty string.")
    
    for book in BOOKS:
        if book.isbn == isbn:
            return book
    raise ResourceNotFoundError("Book", isbn)


def find_member(member_id: str) -> Member:
    """Find a member by ID or raise ResourceNotFoundError."""
    if not member_id or not isinstance(member_id, str):
        raise InvalidInputError("member_id", "Member ID must be a non-empty string.")

    for member in MEMBERS:
        if member.member_id == member_id:
            return member
    raise ResourceNotFoundError("Member", member_id)


def borrow_book(member_id: str, isbn: str, due_date: str) -> Loan:
    """Borrow a book for a member, enforcing business rules."""
    member = find_member(member_id)
    book = find_book(isbn)

    # Rule 1: Check if book is already borrowed
    for loan in LOANS:
        if loan.book.isbn == isbn and not loan.returned:
            raise BusinessRuleError("BOOK_ALREADY_ON_LOAN", f"'{book.title}' is currently borrowed by another member.")

    # Rule 2: Check member loan limit
    active_loans = sum(1 for loan in LOANS if loan.member.member_id == member_id and not loan.returned)
    if active_loans >= member.max_loans:
        raise BusinessRuleError(
            "LOAN_LIMIT_EXCEEDED",
            f"Member {member.name} has reached the maximum loan limit of {member.max_loans}."
        )

    # Create and add new loan
    new_loan = Loan(member=member, book=book, due_date=due_date)
    LOANS.append(new_loan)
    return new_loan


class CatalogueSession:
    """Context Manager wrapping a library catalogue session."""
    def __enter__(self) -> "CatalogueSession":
        print("[SESSION STARTED] Catalogue database connection established.")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        print("[SESSION ENDED] Catalogue session safely closed.")
        # Returning False allows any unhandled non-domain exceptions to propagate normally
        return False
