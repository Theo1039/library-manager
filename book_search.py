def booksearch(library: list) -> None:
    if len(library) == 0:
        print("Your library is empty! Add some books first.")
        return
    search = input("Search book title/author: ").strip().lower()
    if not search:
        print("Enter a search tearm.")
        return
    matches = []
    for book in library:
        if search in book.get('title', '').lower() or search in book.get('author', '').lower():
            matches.append(book)
    if not matches:
        print(f"No matches found for '{search}', try another word.")
        return

    print(f"Found {len(matches)}:")
    for i, book in enumerate(matches, start=1):
        print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
