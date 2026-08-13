
def add_book(library: list):
    title = input("The name of the book is: ").strip().title()
    if title == "":
        print("Title cannot be empty.")
        return
    author = input("The author of the book is: ").strip().title()
    if author == "":
        print("Author cannot be empty.")
        return
    while True:
        year_input = input("The year of publication is: ").strip()
        try:
            year = int(year_input)
        except ValueError:
            print("Please enter a valid 4-digit number.")
            continue
        if 1000 <= year <= 2026:
            break
        else:
            print("Please enter a year between 1000 and 2026")
    genre = input("Enter genre: ").strip().title()
    if genre == "":
        print("Genre cannot be empty.")
        return

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