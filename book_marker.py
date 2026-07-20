#1 book_marker.py - Role 4: The Read-Tracker
def mark_as_read(library):
    """Let's the user pick a book, mark it as read, and rate it 1-5 stars.

    Args:
        library: list of book dictionaries. Each book is a dict with keys:
                 'title', 'author', 'year', 'genre', 'read' (bool), 'rating' (int 0-5).
    """

    #2 Checks if library is empty
    if len(library) == 0:
        print("📭 Your library is empty! Add some books first.")
        return

    #3 Prints a numbered list of books
    print("\n📚 Your Library:")
    print("-" * 40)

    #4 changed the for loop to enumerate to get the index and book
    for i, book in enumerate(library, start=1):
        if book["read"]:
            status = "✓ Already read"
        else:
            status = "○ Not read yet"
        print(f"  {i}. {book['title']} by {book['author']} — {status}")
    print("-" * 40)

    #5 Asks the user for a book number with validation
    while True:
        answer = input("Which book did you finish reading? Enter the number: ")

        # Check if it's actually a number
        try:
            choice = int(answer)
        except ValueError:
            print("❌ That's not a number! Try again.\n")
            continue

        # Check if the number is in valid range
        if 1 <= choice <= len(library):
            break
        else:
            print(f"❌ Please enter a number between 1 and {len(library)}.\n")

    # Convert from user's 1-based number to Python's 0-based index
    book_index = choice - 1
    book = library[book_index]

    #6 Mark the book as read
    book["read"] = True

    #7 Ask the user for a rating between 1-5 with validation
    while True:
        rating_answer = input(f"Rate '{book['title']}' from 1 to 5 stars: ")
        try:
            rating = int(rating_answer)
        except ValueError:
            print("❌ That's not a number! Try again.\n")
            continue
        if 1 <= rating <= 5:
            break
        else:
            print("❌ Please enter a number between 1 and 5.\n")

    book["rating"] = rating

    #8 Convert user rating input to stars
    stars = "★" * rating + "☆" * (5 - rating)

    # Success message
    print(f"\n🎉 Marked '{book['title']}' as read! Rating: {stars}")