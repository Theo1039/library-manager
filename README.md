# 📚 Personal Library Manager

A collaborative command-line (CLI) application for managing your personal book collection — built by a group of 10 Python beginners as a learning project under the **Learn2Earn** fellowship.

You can add books, view your collection, search, mark books as read with a star rating, delete books, see fun statistics, get a random recommendation from your unread pile, maintain a separate wishlist, import/export via CSV, and save your library so it's still there when you re-open the app.

---

## ✨ Features

| # | Feature | Description |
|---|---|---|
| 1 | **Add a Book** | Enter title, author, 4-digit publication year (validated), and genre. Empty inputs are rejected. |
| 2 | **View All Books** | Formatted numbered list with genre, read/unread status, and ★ star rating. Pluralizes "book/books" correctly. |
| 3 | **Search Books** | Case-insensitive search across both titles and authors. |
| 4 | **Mark as Read** | Pick a book from a numbered list, mark it read, rate it 1–5 stars (★). Invalid input is rejected gracefully. |
| 5 | **Delete a Book** | Delete with a y/n confirmation prompt; the updated library is displayed afterwards. |
| 6 | **Statistics** | Total books, % read, average rating of rated books, books-per-genre breakdown, highest/lowest rated, oldest/newest. |
| 7 | **Random Recommendation** | Picks a random unread book when you don't know what to read next. |
| 8 | **Import from CSV** | Bulk-import books from a CSV file using a graphical file picker (with manual path fallback). Detects duplicates by title+author. |
| 9 | **Export to CSV** | Export your entire library to a CSV file openable in Excel / Google Sheets. Uses Python's `csv.writer` for correct escaping. |
| 10 | **Wishlist** | Maintain a separate list of books you want to read; move them to your main library when you get a copy. |
| 11 | **Save & Exit** | Saves both your library and wishlist to `library.json` (handles corrupted JSON by starting fresh). |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10 or higher ([download](https://www.python.org/downloads/))
- Tkinter (ships with Python on Windows/macOS; the CSV importer falls back to manual path entry on Linux systems without it)
- No `pip install` needed — everything uses the standard library.

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/Theo1039/library-manager.git

# 2. Move into the project folder
cd library-manager

# 3. Run the app
python library_manager.py
```
> Use `python3` instead of `python` on Linux/macOS if your system defaults to Python 2.

The app will create `library.json` the first time you save.

---

## 📁 Project Structure

```
library-manager/
├── library_manager.py    # Main entry point — menu loop & module integration (Role 11)
├── book_adder.py         # Role 1  — Add books
├── book_display.py       # Role 2  — Display all books
├── book_search.py        # Role 3  — Search by title/author
├── book_marker.py        # Role 4  — Mark book as read + rate it
├── book_deleter.py       # Role 5  — Delete a book
├── book_statistics.py    # Role 6  — Dashboard statistics
├── recommendation.py     # Role 7  — Random book recommendation
├── csv_importer.py       # Role 8  — Bulk import from CSV (with GUI file picker)
├── csv_exporter.py       # Role 9  — Export library to CSV
├── wishlist.py           # Role 10 — Reading wishlist
└── library.json          # (auto-created) saved library/wishlist data
```

**Architecture:** Each feature lives in its own file exposing one main function. `library_manager.py` imports all modules and wires the 11 menu options to the right function. This split let 11 people work in parallel without overwriting each other's code.

---

## 👥 Team & Contributors

This project was built by 10 Learn2Earn fellows splitting the work by role, with collective bug fixes during integration week:

| Role | Feature | Contributor |
|---|---|---|
| 1 — Book Adder | Add books with year/empty-input validation | [Snrboi](https://github.com/Snrboi) |
| 2 — Book Displayer | Formatted book list with stars and alignment | [Aguimmanuel](https://github.com/Aguimmanuel) |
| 3 — Search | Case-insensitive title/author search | [Piondy](https://github.com/Piondy) |
| 4 — Read Tracker | Mark-as-read + 1–5 star rating | [Aguimmanuel](https://github.com/Aguimmanuel) |
| 5 — Book Deleter | Delete with confirmation + updated view | [favourawo](https://github.com/favourawo) |
| 6 — Statistician | Stats dashboard (genres, averages, extremes) | [ntongho](https://github.com/ntongho) |
| 7 — Recommender | Random unread-book suggestion | rcollins |
| 8 — CSV Importer | GUI file picker, duplicate detection, encoding handling | [okwedavid](https://github.com/okwedavid) |
| 9 — CSV Exporter | Export to properly-formatted CSV | [Chebemeze](https://github.com/Chebemeze) |
| 10 — Wishlist Keeper | Separate wishlist + move-to-library | [Skynkem123](https://github.com/youngbeckdoracle) |
| 11 — Integrator / Lead | `library_manager.py` main loop, JSON persistence, wiring | [Theo1039](https://github.com/Theo1039) |

Repository: [Theo1039/library-manager](https://github.com/Theo1039/library-manager)

---

## 🧠 Python Concepts We Learned

By building this project we got hands-on practice with:

- **Data structures:** Lists (`[]`) for collections, dictionaries (`{}`) for book records
- **Control flow:** `for` loops, `while` loops, `if/elif/else`, `break`, `continue`
- **Functions:** `def`, parameters, return values, docstrings, type hints
- **String handling:** f-strings, `.strip()`, `.title()`, `.lower()`, `.join()`, `.split()`, format specifiers (`:.2f`, `:,`)
- **User I/O:** `input()`, `print()`, formatted aligned columns
- **Error handling:** `try/except` for `ValueError`, `FileNotFoundError`, `json.JSONDecodeError`
- **File I/O:** `with open(...)`, JSON persistence via `json.dump` / `json.load`, CSV via the built-in `csv` module
- **Modules & imports:** Splitting code across multiple files and importing them
- **Standard library:** `random.choice()`, `pathlib.Path`, `tkinter` (file dialog), `csv.reader`/`csv.writer`
- **Collaboration:** Git branches, pull requests, merge conflicts, agreeing on a shared data contract

---

## 📜 The Data Contract

Every module agrees on a single book format — the "data contract." If one module had used `'name'` for title and another `'title'`, the app would have broken on integration day. All modules use this exact dictionary shape:

```python
book = {
    "title":  "The Great Gatsby",   # str
    "author": "F. Scott Fitzgerald",# str
    "year":   1925,                 # int (4-digit)
    "genre":  "Fiction",            # str
    "read":   False,                # bool (True/False)
    "rating": 0                     # int (0 = unrated, 1–5 once rated)
}

library  = []   # list of book dicts (owned books)
wishlist = []   # list of book dicts (want-to-read books, same shape)
```

---

## 🐛 Known Limitations & Future Improvements

The app is fully functional for v1. A few polish items and small UX
improvements remain open for future pull requests:

- **book_marker.py:** Re-marking an already-read book overwrites its rating
  without an "update existing rating?" confirmation prompt.
- **book_deleter.py:** The confirmation prompt only accepts exactly `y`/`Y`.
  Typing `yes` cancels instead of confirming.
- **book_statistics.py:** "Highest rated" / "Lowest rated" and the average
  rating currently include read-but-unrated books (rating = 0), which drags
  the average down and can surface an unrated book as "lowest rated."
- **csv_importer.py:** Imports do not enforce the 1000–current-year range
  that the manual "Add a Book" flow enforces, so out-of-range years can slip
  through bulk imports.
- **wishlist.py:** Author and genre are not validated on input (pressing
  Enter stores them as blank strings), unlike the main "Add a Book" flow.
- **Inconsistent empty-state messages:** A couple of modules use plain
  wording while the rest use the 📭 emoji.
- **Year 2026** is hardcoded in `book_adder.py` and `wishlist.py`; using
  `datetime.date.today().year` would remove the need for a future patch.
- **`.title()` capitalization** can mangle names like "CJ Archer" →
  "Cj Archer". Low priority.
- **`book_display.py`** uses fixed-width columns (`:15s`, `:16s`), so long
  genre or author names push the rating column out of alignment.

---

## 🎉 Acknowledgements

Big thanks to the Learn2Earn fellowship coordinators for the structure and push, and to every teammate who researched a concept, wrote a module, debugged an edge case, or sat through a merge-conflict session on Integration Day. This is our first real Python app, built from scratch together.

*Built with 🐍 by beginners, for beginners.*
