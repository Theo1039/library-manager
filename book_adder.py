
def add_book(library: list):
    title = input("The name of the book is: ").strip().title()
    if title == "":
        print("Title cannot be empty.")
    author = input("The author of the book is: ").strip().title()
    if author == "":
        print("Author cannot be empty.")
    while True:
        year = input("The year of publication is: ").strip()
        if year.isdigit() and len(year) == 4:
            year = int(year)
            break
        else:
            print("Invalid year. Please enter a 4-digit number.")
    genre = input("Enter genre: ").strip().title()
    if genre == "":
        print("Genre cannot be empty.")

    book = {
        "title": title,
        "author":author,
        "year" : year,
        "genre": genre,
        "read": False,
        "rating": 0
    }

    library.append(book)

    print(f"`{title}` by `{author}` has been successfully added")