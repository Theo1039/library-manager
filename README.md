# 📚 Personal Library Manager

A collaborative command-line (CLI) application for managing your personal book collection — built by a group of 11 Python beginners as a learning project under the **Learn2Earn** fellowship.

You can add books, view your collection, search, mark books as read with a star rating, delete books, see fun statistics, get a random recommendation from your unread pile, maintain a separate wishlist, import/export via CSV, and save your library so it's still there when you re-open the app.

---

## ✨ Features

| # | Feature | Description |
|---|---|---|
| 1 | **Add a Book** | Enter title, author, 4-digit publication year, and genre. Year is validated before accepting. |
| 2 | **View All Books** | Nicely formatted numbered list with genre, read/unread status, and star rating. |
| 3 | **Search Books** | Case-insensitive search across titles and authors. |
| 4 | **Mark as Read** | Pick a book from a numbered list, mark it read, and rate it 1–5 stars (★). |
| 5 | **Delete a Book** | Delete with a confirmation prompt; updated library is shown afterwards. |
| 6 | **Statistics** | Total books, % read, average rating, books per genre, highest/lowest rated, oldest/newest. |
| 7 | **Random Recommendation** | Picks a random unread book for you to read next. |
| 8 | **Import from CSV** | Bulk-import books from a CSV file using a graphical file picker (with duplicate detection). |
| 9 | **Export to CSV** | Export your entire library to a CSV file you can open in Excel / Google Sheets. |
| 10 | **Wishlist** | Maintain a separate list of books you want to read later; move them to your main library when you get a copy. |
| 11 | **Save & Exit** | Saves both your library and wishlist to `library.json` so everything persists between sessions. |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10 or higher ([download](https://www.python.org/downloads/))
- No extra installation needed — the only non-stdlib feature used (Tkinter file picker for CSV import) ships with Python by default on Windows/macOS and falls back to manual path entry on Linux systems without Tk.

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/Theo1039/library-manager.git

# 2. Move into the project folder
cd library-manager

# 3. Switch to the develop branch (where all current work lives)
git checkout develop

# 4. Run the app
python library_manager.py
```
> Use `python3` instead of `python` on Linux/macOS if your system defaults to Python 2.

When you first run it, the app will create a `library.json` file in the same folder to store your books.

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
└── library.json          # (auto-created) saved data
```

**Architecture:** Each feature lives in its own file and exposes one main function. `library_manager.py` imports every module and wires the 11 menu options to the right function. This split let 11 people work in parallel without stepping on each other's code.

---

## 👥 Team & Contributors

This project was built by 11 fellows splitting the work by role, plus a few extra bug-fix contributions during integration:

| Role | Feature | Contributor |
|---|---|---|
| 1 — Book Adder | Add books with input validation | [Snrboi](https://github.com/Snrboi) |
| 2 — Book Displayer | Formatted book list with stars | [Aguimmanuel](https://github.com/Aguimmanuel) |
| 3 — Search | Case-insensitive title/author search | [Piondy](https://github.com/Piondy) |
| 4 — Read Tracker | Mark-as-read + 1–5 star rating | [Aguimmanuel](https://github.com/Aguimmanuel) |
| 5 — Book Deleter | Delete with confirmation | [favourawo](https://github.com/favourawo) |
| 6 — Statistician | Stats dashboard (genre breakdown, averages, extremes) | [ntongho](https://github.com/ntongho) |
| 7 — Recommender | Random unread-book suggestion | rcollins |
| 8 — CSV Importer | GUI file picker, duplicate detection, error handling | [okwedavid](https://github.com/okwedavid) |
| 9 — CSV Exporter | Export library to CSV | [Chebemeze](https://github.com/Chebemeze) |
| 10 — Wishlist Keeper | Separate wishlist + move-to-library | [Skynkem123](https://github.com/Skynkem123) |
| 11 — Integrator / Lead | `library_manager.py` main loop, JSON save/load, wiring it all together | [Theo1039](https://github.com/Theo1039) |

Special thanks to everyone who jumped in with last-minute bug fixes during integration.

Repository: [Theo1039/library-manager](https://github.com/Theo1039/library-manager) (active branch: [`develop`](https://github.com/Theo1039/library-manager/tree/develop))

---

## 🧠 Python Concepts We Learned

By building this project we got hands-on practice with:

- **Data structures:** Lists (`[]`) for collections, dictionaries (`{}`) for book records
- **Control flow:** `for` loops, `while` loops, `if/elif/else`, `break`, `continue`
- **Functions:** `def`, parameters, return values, docstrings, type hints
- **String handling:** f-strings, `.strip()`, `.title()`, `.lower()`, `.join()`, `.split()`
- **User I/O:** `input()`, `print()`, formatting aligned columns
- **Error handling:** `try/except` for `ValueError` and `FileNotFoundError`
- **File I/O:** Opening/reading/writing files with `with open(...)`, JSON persistence via `json.dump` / `json.load`, CSV via the `csv` module
- **Modules & imports:** Splitting code across multiple files and importing them
- **The standard library:** `random.choice()`, `pathlib.Path`, `tkinter` (file dialog), `csv`
- **Collaboration:** Git branches, pull requests, merge conflicts, and agreeing on a shared data contract before writing code

---

## 📜 The Data Contract

Every module agrees on a single book format — we called this the "data contract." If one person's module used `'name'` for title and another used `'title'`, the app would break on integration day. So we all committed to this exact dictionary shape:

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
wishlist = []   # list of book dicts (books to read later, same shape)
```

---

## 🐛 Known Issues & Final Touches (to-do before merging to main)

A few small things that could still be polished — good first fixes for anyone reading this after the project:

- [ ] **Menu typo:** Option 8 currently says *"Import book books from a CSV"* — should be *"Import books from a CSV"*.
- [ ] **Success-message typo in `book_adder.py`:** *"succesfully added"* → *"successfully added"*.
- [ ] **Punctuation in `book_search.py`:** The "no matches" message has a stray apostrophe: `"try another word.'"` → `"try another word."`
- [ ] **Empty-library bug in `recommendation.py`:** When the library has zero books it prints *"HURRAY!!! You have read all the books"* — it should first check for an empty library and print a different message.
- [ ] **CSV export doesn't escape commas:** In `csv_exporter.py`, if a book title or author contains a comma (e.g. `"The Road, Part 1"`), the CSV output will break columns. Using Python's built-in `csv.writer` (the same way `csv_importer.py` uses `csv.reader`) would fix it cleanly.
- [ ] **`book_deleter.py` indentation:** A few lines have inconsistent extra spacing (still runs, but is hard to read). Clean up the comments and leftover commented-out test code at the bottom.
- [ ] **Minor comment typo:** `book_marker.py` line 1 says `#1` instead of `#` and the docstring says *"Let's the user"* — should be *"Lets the user"*.
- [ ] **Add a `.gitignore`:** The `__pycache__/` folder and `library.json` (personal user data) shouldn't be committed to the repo. A `.gitignore` with at least:
  ```
  __pycache__/
  *.pyc
  library.json
  .env
  ```
  would clean that up.

---

## 🎉 Acknowledgements

Big thanks to the Learn2Earn fellowship coordinators for the push, and to every team member who researched a concept, wrote a module, debugged an edge case, or sat through a merge-conflict session on Integration Day. This is our first real Python app, built from scratch together.

*Built with 🐍 by beginners, for beginners.*
