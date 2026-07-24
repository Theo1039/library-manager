def export_books(library: list, filename: str = "library_export.csv"):
    if not library:
        print("You entered an empty library. Add books to library first")
        return

    with open(filename, "w") as f:
        csv_list = ["title", "author", "year", "genre", "read", "rating"]
        f.write(','.join(csv_list) + "\n")

    for book in library:
        csv_list = [book["title"], book["author"], str(book["year"]), book["genre"], str(book["read"]), str(book["rating"])]

        with open(filename, "a") as f:
            f.write(','.join(csv_list) + "\n")

    print(f"📤 Successfully exported {len(library)} book(s) to {filename}!")
