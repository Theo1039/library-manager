# book_display.py - Role 2: The Book Displayer
def display_books(library: list):
    """Displays all books in the library in a clean, numbered, formatted list.

    Args:
        library: list of book dictionaries. Each book is a dict with keys:
                 'title', 'author', 'year', 'genre', 'read' (bool), 'rating' (int 0-5).
    """

    # 1 Check if library is empty
    if len(library) == 0:
        print("📭 Your library is empty! Add some books first.")
        return

    # 2 Print header with total book count (handles plural correctly)
    total = len(library)
    book_word = "book" if total == 1 else "books"
    print(f"\n📚 Your Library ({total} {book_word})")
    print("-" * 90)

    # 3 Loop through every book with 1-based numbering
    for i, book in enumerate(library, start=1):
        # Match the same status wording used in book_marker
        if book["read"]:
            status = "✓ Already read"
        else:
            status = "○ Not read yet"

        # Same star system as book_marker for consistency
        if book["rating"] == 0:
            stars = "—"
        else:
            stars = "★" * book["rating"] + "☆" * (5 - book["rating"])

        # Print main book line
        print(f"  {i}. {book['title']} by {book['author']} ({book['year']})  Genre: {book['genre']:15s}  Status: {status:16s}  Rating: {stars}")

    # 4 Closing divider
    print("-" * 90)
