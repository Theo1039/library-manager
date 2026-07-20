

library = []

def add_book(library):
    title = input("The name of the book is: ").strip().title()
    author = input("The author of the book is: ").strip().title()
    year = int(input("It was produced in : "))
    genre = input("Enter genre: ").strip().title()

    book = {
        "title": title,
        "author":author,
        "year" : year,
        "genre": genre,
        "read": False,
        "rating": 0
    }

    library.append(book)

    print(f"`{title}` by `{author}` has been succesfully added")

add_book(library)