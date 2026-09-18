# ==============================================================================
# Day 2: Bookstore Inventory Analyser (Simple & Beginner-Friendly Version)
# Concepts: list, dict, set, tuple, comprehensions, built-ins (enumerate, sorted, etc.)
# ==============================================================================

# 1. INITIAL STOCK DATA
# Book structure (tuple): (title, author, genre, year, price)
# Why tuple? A single book record is fixed and shouldn't change (immutable).
# Why list? Inventory is an ordered list of books that can change (mutable).
raw_inventory = [
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, 14.99),
    ("The Fellowship of the Ring", "J.R.R. Tolkien", "Fantasy", 1954, 16.99),
    ("The Two Towers", "J.R.R. Tolkien", "Fantasy", 1954, 16.99),
    ("1984", "George Orwell", "Dystopian", 1949, 12.50),
    ("Animal Farm", "George Orwell", "Dystopian", 1945, 9.99),
    ("1984", "George Orwell", "Dystopian", 1949, 12.50),  # Duplicate record
    ("Brave New World", "Aldous Huxley", "Dystopian", 1932, 13.99),
    ("Dune", "Frank Herbert", "Sci-Fi", 1965, 18.50),
    ("Dune Messiah", "Frank Herbert", "Sci-Fi", 1969, 15.00),
    ("Neuromancer", "William Gibson", "Sci-Fi", 1984, 11.25),
    ("Foundation", "Isaac Asimov", "Sci-Fi", 1951, 10.99),
    ("The Shining", "Stephen King", "Horror", 1977, 14.50),
    ("It", "Stephen King", "Horror", 1986, 17.99),
    ("The Shining", "Stephen King", "Horror", 1977, 14.50),  # Duplicate record
    ("Misery", "Stephen King", "Horror", 1987, 13.25),
    ("Dracula", "Bram Stoker", "Horror", 1897, 8.99)
]

print("=== 1. ORIGINAL INVENTORY SUMMARY ===")
print(f"Total records in raw inventory: {len(raw_inventory)}\n")


# 2. DE-DUPLICATION PASS (USING A SET & SIMPLE FOR LOOP)
# A 'set' stores UNIQUE items and provides fast lookups.
# We track seen (title, author) tuples in a set to identify duplicates.
seen_books = set()
inventory = []
duplicates_removed = []

for book in raw_inventory:
    title, author, genre, year, price = book
    key = (title, author)
    if key in seen_books:
        duplicates_removed.append(book)
    else:
        seen_books.add(key)
        inventory.append(book)

print("=== 2. DE-DUPLICATION PASS ===")
print(f"Removed {len(duplicates_removed)} duplicate record(s):")
for title, author, genre, year, price in duplicates_removed:
    print(f" - Removed: '{title}' by {author} (Duplicate entry found)")
print(f"Working inventory count after de-duplication: {len(inventory)}\n")


# 3. GENRE REPORT (USING SET COMPREHENSION & DICTIONARIES)
# Extract unique genres using a Set Comprehension { ... }
genres = sorted({book[2] for book in inventory})

# For each genre, compute statistics
genre_report = {}
for genre in genres:
    # Filter books matching this genre using List Comprehension [ ... ]
    books_in_genre = [b for b in inventory if b[2] == genre]
    
    total_titles = len(books_in_genre)
    avg_price = round(sum(b[4] for b in books_in_genre) / total_titles, 2)
    
    # Find the most recent book using max() with key=lambda
    latest_book = max(books_in_genre, key=lambda b: b[3])
    
    genre_report[genre] = {
        "total_titles": total_titles,
        "avg_price": avg_price,
        "latest_title": latest_book[0],
        "latest_year": latest_book[3]
    }

print("=== 3. GENRE REPORT ===")
for genre, data in genre_report.items():
    print(f"Genre: {genre:<10} | Titles: {data['total_titles']:<2} | Avg Price: ${data['avg_price']:<5.2f} | Latest: '{data['latest_title']}' ({data['latest_year']})")
print()


# 4. AUTHOR TO TITLES MAPPING (USING DICTIONARY ITERATION)
author_to_titles = {}
for title, author, genre, year, price in inventory:
    if author not in author_to_titles:
        author_to_titles[author] = []
    author_to_titles[author].append(title)

print("=== 4. AUTHOR TO TITLES MAPPING ===")
for author, titles in author_to_titles.items():
    print(f" - {author}: {', '.join(titles)}")
print()


# 5. UNIQUE AUTHORS & REPEAT AUTHORS ANALYSIS
# List Comprehension: get a list of all author names
all_authors_list = [book[1] for book in inventory]

# Convert list to set for unique authors
unique_authors = set(all_authors_list)

# Set Comprehension: find authors appearing more than once
repeat_authors = {author for author in unique_authors if all_authors_list.count(author) > 1}

print("=== 5. AUTHOR SETS ANALYSIS ===")
print(f"All Unique Authors ({len(unique_authors)}): {', '.join(sorted(unique_authors))}")
print(f"Authors with Multiple Titles ({len(repeat_authors)}): {', '.join(sorted(repeat_authors))}")
