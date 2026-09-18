# Day 4: Library Catalogue - Part 2 (Domain Models)
# Topics: OOP, Classes, @dataclass, @property, Inheritance, super(), dunder methods

from dataclasses import dataclass
from typing import Optional, Callable


# 1. DOMAIN MODELS

@dataclass
class Book:
    """Dataclass representing a book in the library catalogue."""
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
        """Computed property: returns True if loan is not returned and today is past due_date."""
        # Using fixed reference date for demo consistency matching Day 3
        current_date = "2026-09-15"
        return not self.returned and self.due_date < current_date

    def __str__(self) -> str:
        status = "Returned" if self.returned else ("OVERDUE" if self.is_overdue else "Active")
        return f"Loan({self.member.name} -> '{self.book.title}', Due: {self.due_date}, Status: {status})"


# 2. HARDCODED INSTANCE DATA

BOOKS: list[Book] = [
    Book("978-0141439518", "Pride and Prejudice", "Jane Austen", 1813),
    Book("978-0451524935", "1984", "George Orwell", 1949),
    Book("978-0061120084", "To Kill a Mockingbird", "Harper Lee", 1960),
    Book("978-0141439587", "Emma", "Jane Austen", 1815),
    Book("978-0345339706", "The Hobbit", "J.R.R. Tolkien", 1937),
]

MEMBERS: list[Member] = [
    Member("M001", "Alice"),
    Member("M002", "Bob"),
    PremiumMember("M003", "Charlie"),
]

LOANS: list[Loan] = [
    Loan(member=MEMBERS[0], book=BOOKS[0], due_date="2026-09-10", returned=False),
    Loan(member=MEMBERS[0], book=BOOKS[1], due_date="2026-09-20", returned=False),
    Loan(member=MEMBERS[1], book=BOOKS[2], due_date="2026-09-01", returned=False),
    Loan(member=MEMBERS[2], book=BOOKS[3], due_date="2026-08-15", returned=True, return_date="2026-08-14"),
]


# 3. TYPED DOMAIN FUNCTIONS

def lookup_book_by_isbn(isbn: str) -> Optional[Book]:
    """Find a Book instance by ISBN. Returns None if missing."""
    for book in BOOKS:
        if book.isbn == isbn:
            return book
    return None


def get_books_by_author(author_name: str) -> list[Book]:
    """Return a list of Book instances by a given author."""
    return [book for book in BOOKS if book.author.lower() == author_name.lower()]


def has_overdue_loans(member_id: str) -> bool:
    """Return True if the member has any unreturned overdue loans."""
    for loan in LOANS:
        if loan.member.member_id == member_id and loan.is_overdue:
            return True
    return False


def calculate_fine(days_overdue: int, *, rate_per_day: float = 0.50) -> float:
    """Calculate fine for overdue days."""
    if days_overdue <= 0:
        return 0.0
    return round(days_overdue * rate_per_day, 2)


def format_books(books: list[Book], transform_fn: Callable[[Book], str]) -> list[str]:
    """Apply transform_fn to each Book instance."""
    return [transform_fn(book) for book in books]


# 4. MAIN ENTRY POINT & TERMINAL REPORT

def main() -> None:
    print("=== PUBLIC LIBRARY CATALOGUE (PART 2 - DOMAIN MODELS) ===")
    print()

    # 1. ISBN Lookup Test
    print("1. ISBN Lookup")
    found_book = lookup_book_by_isbn("978-0451524935")
    if found_book:
        print(f"Found: {found_book}")
    else:
        print("Book not found!")

    missing_book = lookup_book_by_isbn("978-0000000000")
    if missing_book is None:
        print("Lookup for '978-0000000000': Not Found (None)")
    print()

    # 2. Author Search Test
    print("2. Books by Author")
    austen_books = get_books_by_author("Jane Austen")
    for b in austen_books:
        print(f"- {b}")
    print()

    # 3. Overdue Check Test using Computed Property
    print("3. Overdue Loans Check")
    for m in MEMBERS:
        is_overdue = has_overdue_loans(m.member_id)
        print(f"{m.name} ({m.member_id}): {'Overdue Loans Found!' if is_overdue else 'No Overdue Loans'}")
    print()

    # 4. Fine Calculation Test
    print("4. Fine Calculation")
    print(f"5 days overdue (Default rate $0.50): ${calculate_fine(5):.2f}")
    print(f"5 days overdue (Custom rate $1.25) : ${calculate_fine(5, rate_per_day=1.25):.2f}")
    print()

    # 5. Callable Transformation Test
    print("5. Formatted Books List (Using Callable)")
    def custom_formatter(b: Book) -> str:
        return f"[CATALOGUE ITEM] {b.title.upper()} - Written by {b.author}"

    for line in format_books(BOOKS, custom_formatter):
        print(line)


if __name__ == "__main__":
    main()
