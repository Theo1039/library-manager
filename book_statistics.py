"""
statistics.py
-------------
Role 6: The Statistician

Provides show_statistics(library) — calculates and prints summary
stats about the user's book collection.

Follows the shared data contract: each book is a dict with keys
'title', 'author', 'year', 'genre', 'read' (bool), 'rating' (0-5 int).
"""


def show_statistics(library: list) -> None:
    """Calculate and display statistics about the library.

    Handles the empty-library case and the "no books read yet" case
    (which would otherwise cause a division by zero when averaging
    ratings).
    """
    total = len(library)

    print("\n📊 Library Statistics")
    print("─" * 23)

    # Guard clause: nothing to calculate if there are no books at all.
    if total == 0:
        print("Your library is empty — add some books first!")
        return

    print(f"Total books:    {total}")

    # --- Read / Unread counts -------------------------------------
    # Accumulator pattern: walk the list once, count as we go.
    read_count = 0
    for book in library:
        if book["read"]:
            read_count += 1

    unread_count = total - read_count

    # round() keeps the percentage readable (no long decimals).
    read_pct = round((read_count / total) * 100)
    unread_pct = round((unread_count / total) * 100)

    print(f"Read:           {read_count} ({read_pct}%)")
    print(f"Unread:         {unread_count} ({unread_pct}%)")

    # --- Average rating of READ books only --------------------------
    # Conditional aggregation: only sum ratings for books marked read.
    rating_sum = 0
    rated_book_count = 0
    for book in library:
        if book["read"]:
            rating_sum += book["rating"]
            rated_book_count += 1

    if rated_book_count == 0:
        # Avoids ZeroDivisionError — nothing has been read yet.
        print("Average rating: No rated books yet")
    else:
        avg_rating = round(rating_sum / rated_book_count, 1)
        print(f"Average rating: {avg_rating} ★")

    # --- Books per genre --------------------------------------------
    # Frequency dictionary pattern: count occurrences of each genre.
    genre_counts = {}
    for book in library:
        genre = book["genre"]
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    print("Books by genre:")
    for genre, count in genre_counts.items():
        print(f"  {genre}:{' ' * max(1, 12 - len(genre))}{count}")

    # --- Bonus: highest/lowest rated + oldest/newest -----------------
    read_books = [b for b in library if b["read"]]
    if read_books:
        highest = max(read_books, key=lambda b: b["rating"])
        lowest = min(read_books, key=lambda b: b["rating"])
        print(f"\nHighest rated:  '{highest['title']}' ({highest['rating']} ★)")
        print(f"Lowest rated:   '{lowest['title']}' ({lowest['rating']} ★)")

    oldest = min(library, key=lambda b: b["year"])
    newest = max(library, key=lambda b: b["year"])
    print(f"Oldest book:    '{oldest['title']}' ({oldest['year']})")
    print(f"Newest book:    '{newest['title']}' ({newest['year']})")