# library = []
def add_book(library: list):
    while True:
        title = input("The name of the book is: ").strip().title()
        if not title:
            print("Title cannot be empty.")
            continue
        else:
            break
    while True:
        author = input("The author of the book is: ").strip().title()
        if not author:
            print("Author cannot be empty.")
            continue
        else:
            break
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
    while True:
        genre = input("Enter genre: ").strip().title()
        if not genre:
            print("Genre cannot be empty.")
            continue
        else:
            break                            

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


# add_book(library)    