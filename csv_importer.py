# csv_importer.py
#ROLE 8

from __future__ import annotations
import csv                          # Reads and writes CSV data files
from pathlib import Path            # Simplifies working with file and folder paths


#Connects Python to the computer's built-in window system.
#This opens a file selection window that works on any computer.

def choose_csv_files(multiple: bool = True) -> list[str]:
    """
    Opens the OS file picker so the user can select one or more CSV files.
    Returns a list of selected file paths (empty list if canceled).

    If tkinter is unavailable, falls back to manual file path entry.
    """
    try:
        from tkinter import Tk, filedialog

        root = Tk()
        root.withdraw()
        root.update()

        filetypes = [("CSV files", "*.csv")]

        if multiple:
            paths = filedialog.askopenfilenames(
                title="Select CSV file(s) to import",
                filetypes=filetypes
            )
        else:
            single = filedialog.askopenfilename(
                title="Select a CSV file to import",
                filetypes=filetypes
            )
            paths = (single,) if single else ()

        root.destroy()
        return list(paths)

    except Exception:
        print("\n⚠️ Graphical file picker is unavailable.")
        print("Please enter the full path(s) to your CSV file(s).")

        if multiple:
            raw = input("CSV file paths (comma separated): ").strip()
            if not raw:
                return []
            return [p.strip().strip('"').strip("'") for p in raw.split(",") if p.strip()]
        else:
            path = input("CSV file path: ").strip().strip('"').strip("'")
            return [path] if path else []


def import_books_from_files(
    library: list,
    file_paths: list[str],
    skip_duplicates: bool = True
) -> None:
    """
    Imports books from the given CSV file paths into `library`.

    Supports:
        title,author,year,genre,read,rating
        Title,Author,Genre,Year,Read,Rating

    Also supports older 4-column CSV files:
        title,author,year,genre
        Title,Author,Genre,Year

    Missing read/rating values default to:
        read = False
        rating = 0

    If skip_duplicates is True:
      duplicates are detected by (title + author) case-insensitively.
    """
    if not file_paths:
        print("⚠️ No files selected.")
        return

    total_imported = 0
    total_skipped = 0

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {path}")
            continue

        imported_count = 0
        skipped_count = 0

        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)

                # Read header so we can determine the column order.
                header = next(reader, None)

                if not header:
                    continue

                header = [column.strip().lower() for column in header]

                # Determine column positions from the header.
                try:
                    title_index = header.index("title")
                    author_index = header.index("author")
                    year_index = header.index("year")
                    genre_index = header.index("genre")
                except ValueError:
                    print(f"❌ Invalid CSV header in '{path.name}'.")
                    continue

                # read/rating may not exist in older 4-column CSV files.
                read_index = header.index("read") if "read" in header else None
                rating_index = header.index("rating") if "rating" in header else None

                for row in reader:
                    if not row:
                        continue

                    # Make sure the required columns exist.
                    required_indexes = [
                        title_index,
                        author_index,
                        year_index,
                        genre_index
                    ]

                    if any(index >= len(row) for index in required_indexes):
                        continue

                    title = row[title_index].strip()
                    author = row[author_index].strip()
                    year_str = row[year_index].strip()
                    genre = row[genre_index].strip()

                    if not title or not author:
                        continue

                    # Validate year.
                    try:
                        year = int(year_str)
                    except ValueError:
                        print(
                            f"⚠️ Skipping '{title}': "
                            f"invalid year '{year_str}'"
                        )
                        continue

                    # Import read value if present.
                    if read_index is not None and read_index < len(row):
                        read_value = row[read_index].strip().lower()

                        if read_value in ("true", "1", "yes"):
                            read = True
                        elif read_value in ("false", "0", "no"):
                            read = False
                        else:
                            read = False
                    else:
                        read = False

                    # Import rating if present.
                    if rating_index is not None and rating_index < len(row):
                        rating_value = row[rating_index].strip()

                        try:
                            rating = int(rating_value)
                        except ValueError:
                            rating = 0
                    else:
                        rating = 0

                    if skip_duplicates:
                        exists = any(
                            b.get("title", "").lower() == title.lower()
                            and b.get("author", "").lower() == author.lower()
                            for b in library
                        )

                        if exists:
                            skipped_count += 1
                            continue

                    library.append({
                        "title": title,
                        "author": author,
                        "year": year,
                        "genre": genre,
                        "read": read,
                        "rating": rating
                    })

                    imported_count += 1

        except Exception as e:
            print(f"❌ Error importing from '{path}': {e}")
            continue

        print(
            f"📥 Imported {imported_count} book(s) from {path.name}!"
            + (
                f" (skipped {skipped_count} duplicate(s))"
                if skip_duplicates else ""
            )
        )

        total_imported += imported_count
        total_skipped += skipped_count

    if skip_duplicates:
        print(
            f"✅ Done. Total imported: {total_imported}, "
            f"total skipped: {total_skipped}"
        )
    else:
        print(f"✅ Done. Total imported: {total_imported}")

#Connects the user interface buttons to the main program logic.
#This is the main function that takes the chosen files and imports the books.
def import_books_csv(
    library: list,
    skip_duplicates: bool = True,
    multiple: bool = True
) -> None:
    """
    User picks CSV file(s) via file explorer, then import into `library`.
    """
    file_paths = choose_csv_files(multiple=multiple)
    import_books_from_files(
        library,
        file_paths,
        skip_duplicates=skip_duplicates
    )


if __name__ == "__main__":
    library: list = []
    import_books_csv(
        library,
        skip_duplicates=True,
        multiple=True
    )
    print(f"Imported {len(library)} book(s).")