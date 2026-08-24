import csv

def export_books(library: list, filename: str = "library_export.csv"):
    if not library:
        print("You entered an empty library. Add books to library first")
        return

    # Open the file once for the entire operation
    # newline="" prevents empty blank lines between rows on Windows
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Write the header row
        headers = ["title", "author", "year", "genre", "read", "rating"]
        writer.writerow(headers)

        # Loop through library and let csv.writer handle escaping safely
        for book in library:
            row = [
                book["title"], 
                book["author"], 
                str(book["year"]), 
                book["genre"], 
                str(book["read"]), 
                str(book["rating"])
            ]
            writer.writerow(row)

    print(f"📤 Successfully exported {len(library)} book(s) to {filename}!")
