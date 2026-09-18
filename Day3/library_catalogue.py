
# Day 3: Command-Line Library Catalogue


from typing import Callable, Optional
# 1. HARDCODED DATA
# Books stored as simple dictionaries in a list
BOOKS: list[dict] = [
    {"isbn": "978-0141439518", "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
    {"isbn": "978-0451524935", "title": "1984", "author": "George Orwell", "year": 1949},
    {"isbn": "978-0061120084", "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"isbn": "978-0141439587", "title": "Emma", "author": "Jane Austen", "year": 1815},
    {"isbn": "978-0345339706", "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
]

# Loans stored as simple dictionaries in a list
LOANS: list[dict] = [
    {"member_id": "M001", "isbn": "978-0141439518", "due_date": "2026-09-10", "returned": False},
    {"member_id": "M001", "isbn": "978-0451524935", "due_date": "2026-09-20", "returned": False},
    {"member_id": "M002", "isbn": "978-0061120084", "due_date": "2026-09-01", "returned": False},
    {"member_id": "M003", "isbn": "978-0141439587", "due_date": "2026-08-15", "returned": True},
]

# 2. SIMPLE TYPED FUNCTIONS

# 1. Look up a book by ISBN (returns book dict or None if missing)
def lookup_book_by_isbn(isbn: str) -> Optional[dict]:
    """Find a book by ISBN. Returns None if not found."""
    for book in BOOKS:
        if book["isbn"] == isbn:
            return book
    return None


# 2. Get all books by a given author
def get_books_by_author(author_name: str) -> list[dict]:
    """Return a list of books written by a specific author."""
    result = []
    for book in BOOKS:
        if book["author"].lower() == author_name.lower():
            result.append(book)
    return result


# 3. Check if a member has overdue loans
def has_overdue_loans(member_id: str, current_date: str) -> bool:
    """Return True if member has any unreturned loan past current_date."""
    for loan in LOANS:
        if loan["member_id"] == member_id and not loan["returned"]:
            if loan["due_date"] < current_date:
                return True
    return False


# 4. Calculate fine for overdue days (with keyword-only arg and default rate)
def calculate_fine(days_overdue: int, *, rate_per_day: float = 0.50) -> float:
    """Calculate fine. `rate_per_day` is keyword-only with default 0.50."""
    if days_overdue <= 0:
        return 0.0
    return round(days_overdue * rate_per_day, 2)


# 5. Transform books list using a Callable (function passed as argument)
def format_books(books: list[dict], transform_fn: Callable[[dict], str]) -> list[str]:
    """Apply transform_fn to each book dictionary and return formatted strings."""
    formatted = []
    for book in books:
        formatted.append(transform_fn(book))
    return formatted



# 3. MAIN ENTRY POINT & TERMINAL REPORT
def main() -> None:
    print(" PUBLIC LIBRARY CATALOGUE ")
    print()

    # 1. ISBN Lookup Test
    print("1.ISBN Lookup")
    book = lookup_book_by_isbn("978-0451524935")
    if book is not None:
        print(f"Found: '{book['title']}' by {book['author']}")
    else:
        print("Book not found!")

    missing = lookup_book_by_isbn("978-0000000000")
    if missing is None:
        print("Lookup for '978-0000000000': Not Found (None)")
    print()

    # 2. Author Search Test
    print("2.Books by Author ")
    austen_books = get_books_by_author("Jane Austen")
    for b in austen_books:
        print(f"- {b['title']} ({b['year']})")
    print()

    # 3. Overdue Check Test
    print("3.Overdue Loans Check ")
    today = "2026-09-15"
    for member in ["M001", "M002", "M003"]:
        overdue = has_overdue_loans(member, today)
        print(f"Member {member}: {'Overdue Loans Found!' if overdue else 'No Overdue Loans'}")
    print()

    # 4. Fine Calculation Test
    print("4.Fine Calculation ")
    print(f"5 days overdue (Default rate $0.50): ${calculate_fine(5):.2f}")
    print(f"5 days overdue (Custom rate $1.25) : ${calculate_fine(5, rate_per_day=1.25):.2f}")
    print()

    # 5. Callable Transformation Test
    print("5.Formatted Books List (Using Callable) ")
    def my_formatter(b: dict) -> str:
        return f"[BOOK] {b['title']} - {b['author']} ({b['year']})"

    formatted_output = format_books(BOOKS, my_formatter)
    for text in formatted_output:
        print(text)


if __name__ == "__main__":
    main()
