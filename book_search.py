def booksearch(library: list) -> None:
    search = input("Search book title/author: ").strip().lower()

    matches = []
    for book in library:
        if search in book['title'].lower() or search in book['author'].lower():
            matches.append(book)
    if not matches:
        print(f"No matches found for '{search}', try another word.'")
        return

    print(f"Found {len(matches)}:")
    for i, book in enumerate(matches, start=1):
        print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
if __name__ == "__main__":
    library = [
        {"title": "How to Play The Piano", "author": "Pius Goodhead", "year": 2026, "genre": "Music"},
        {"title": "Metaphysical Reasoning", "author": "Favor Awo", "year": 2023, "genre": "Life"},
        {"title": "Is AI Serving you? Or is it your Master?", "author": "Theophilus Sunday", "year": 2024, "genre": "religion"},
        {"title": "How to play guitar", "author": "Golden Ometo", "year": 2013, "genre": "Music"},
        {"title": "How to play Flute", "author": "Pius Goodhead", "year": 2013, "genre": "Music"},
    ]
booksearch(library)