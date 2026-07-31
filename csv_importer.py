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


#Loads files from the computer hard drive directly into memory.
#It reads the data, skips the header row, fixes number formats, and removes duplicate entries.

def import_books_from_files(
    library: list,
    file_paths: list[str],
    skip_duplicates: bool = True
) -> None:
    """
    Imports books from the given CSV file paths into `library`.

    Expected CSV format per row:
        title,author,year,genre

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

                # Skip header row (assumed to be first line)
                next(reader, None)

                for row in reader:
                    if not row or len(row) < 4:
                        continue

                    title, author, year_str, genre = (c.strip() for c in row[:4])
                    if not title or not author:
                        continue

                    try:
                        year = int(year_str)
                    except ValueError:
                        print(f"⚠️ Skipping '{title}': invalid year '{year_str}'")
                        continue

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
                        "read": False,
                        "rating": 0
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
        print(f"✅ Done. Total imported: {total_imported}, total skipped: {total_skipped}")
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