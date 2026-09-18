"""CLI Entry Point with Exception Handling."""

from Day5.service import find_book, borrow_book, CatalogueSession
from Day5.exceptions import LibraryError


def main() -> None:
    print("=== LIBRARY CATALOGUE CLI (PART 3) ===")
    print()

    # Wrap operation inside context manager
    with CatalogueSession():
        print()

        # Test 1: Successful Lookup
        try:
            print("1. Searching for valid book (ISBN: 978-0141439518)...")
            book = find_book("978-0141439518")
            print(f"   Success -> {book}")
        except LibraryError as e:
            print(f"   Error -> {e}")
        print()

        # Test 2: Missing Resource (ResourceNotFoundError)
        try:
            print("2. Searching for non-existent book (ISBN: 978-0000000000)...")
            find_book("978-0000000000")
        except LibraryError as e:
            print(f"   Caught Domain Error cleanly -> {e}")
        print()

        # Test 3: Business Rule Violation (Loan Limit Exceeded)
        try:
            print("3. Alice (Limit: 1) attempting to borrow a 2nd book...")
            borrow_book(member_id="M001", isbn="978-0451524935", due_date="2026-09-30")
        except LibraryError as e:
            print(f"   Caught Domain Error cleanly -> {e}")
        print()

        # Test 4: Invalid Input (InvalidInputError)
        try:
            print("4. Attempting lookup with empty ISBN...")
            find_book("")
        except LibraryError as e:
            print(f"   Caught Domain Error cleanly -> {e}")
        print()


if __name__ == "__main__":
    main()
