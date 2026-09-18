"""Domain models for Book, Member, PremiumMember, and Loan."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """Dataclass representing a book in the catalogue."""
    isbn: str
    title: str
    author: str
    year: int

    def __str__(self) -> str:
        return f"Book('{self.title}' by {self.author} [{self.year}], ISBN: {self.isbn})"


class Member:
    """Standard class representing a library member."""
    def __init__(self, member_id: str, name: str, max_loans: int = 3) -> None:
        self.member_id = member_id
        self.name = name
        self.max_loans = max_loans

    def __str__(self) -> str:
        return f"Member({self.member_id}: {self.name}, Max Loans: {self.max_loans})"


class PremiumMember(Member):
    """Subclass extending Member with higher loan limits."""
    def __init__(self, member_id: str, name: str, max_loans: int = 10, priority_support: bool = True) -> None:
        super().__init__(member_id=member_id, name=name, max_loans=max_loans)
        self.priority_support = priority_support

    def __str__(self) -> str:
        return f"PremiumMember({self.member_id}: {self.name}, Max Loans: {self.max_loans}, Priority: {self.priority_support})"


@dataclass
class Loan:
    """Dataclass capturing a loan transaction between a member and a book."""
    member: Member
    book: Book
    due_date: str
    returned: bool = False
    return_date: Optional[str] = None

    @property
    def is_overdue(self) -> bool:
        current_date = "2026-09-15"
        return not self.returned and self.due_date < current_date

    def __str__(self) -> str:
        status = "Returned" if self.returned else ("OVERDUE" if self.is_overdue else "Active")
        return f"Loan({self.member.name} -> '{self.book.title}', Due: {self.due_date}, Status: {status})"
