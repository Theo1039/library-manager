📚 Personal Library Manager
A collaborative command-line (CLI) application for managing your personal book collection — built by a group of 11 Python beginners as a learning project under the Learn2Earn fellowship.

You can add books, view your collection, search, mark books as read with a star rating, delete books, see fun statistics, get a random recommendation from your unread pile, maintain a separate wishlist, import/export via CSV, and save your library so it's still there when you re-open the app.

✨ Features
#	Feature	Description
1	Add a Book	Enter title, author, 4-digit publication year (validated), and genre. Empty inputs are rejected.
2	View All Books	Formatted numbered list with genre, read/unread status, and ★ star rating. Pluralizes "book/books" correctly.
3	Search Books	Case-insensitive search across both titles and authors.
4	Mark as Read	Pick a book from a numbered list, mark it read, rate it 1–5 stars (★). Invalid input is rejected gracefully.
5	Delete a Book	Delete with a y/n confirmation prompt; the updated library is displayed afterwards.
6	Statistics	Total books, % read, average rating of rated books, books-per-genre breakdown, highest/lowest rated, oldest/newest.
7	Random Recommendation	Picks a random unread book when you don't know what to read next.
8	Import from CSV	Bulk-import books from a CSV file using a graphical file picker (with manual path fallback). Detects duplicates by title+author.
9	Export to CSV	Export your entire library to a CSV file openable in Excel / Google Sheets. Uses Python's csv.writer for correct escaping.
10	Wishlist	Maintain a separate list of books you want to read; move them to your main library when you get a copy.
11	Save & Exit	Saves both your library and wishlist to library.json (handles corrupted JSON by starting fresh).
🚀 How to Run
Prerequisites
Python 3.10 or higher (download)
Tkinter (ships with Python on Windows/macOS; the CSV importer falls back to manual path entry on Linux systems without it)
No pip install needed — everything uses the standard library.
Steps
Bash

# 1. Clone the repository
git clone https://github.com/Theo1039/library-manager.git

# 2. Move into the project folder
cd library-manager

# 3. Switch to the develop branch (where all current work lives)
git checkout develop

# 4. Run the app
python library_manager.py
Use python3 instead of python on Linux/macOS if your system defaults to Python 2.

The app will create library.json the first time you save.

📁 Project Structure
text

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
Architecture: Each feature lives in its own file exposing one main function. library_manager.py imports all modules and wires the 11 menu options to the right function. This split let 11 people work in parallel without overwriting each other's code.

👥 Team & Contributors
This project was built by 11 Learn2Earn fellows splitting the work by role, with collective bug fixes during integration week:

Role	Feature	Contributor
1 — Book Adder	Add books with year/empty-input validation	Snrboi
2 — Book Displayer	Formatted book list with stars and alignment	Aguimmanuel
3 — Search	Case-insensitive title/author search	Piondy
4 — Read Tracker	Mark-as-read + 1–5 star rating	Aguimmanuel
5 — Book Deleter	Delete with confirmation + updated view	favourawo
6 — Statistician	Stats dashboard (genres, averages, extremes)	ntongho
7 — Recommender	Random unread-book suggestion	rcollins
8 — CSV Importer	GUI file picker, duplicate detection, encoding handling	okwedavid
9 — CSV Exporter	Export to properly-formatted CSV	Chebemeze
10 — Wishlist Keeper	Separate wishlist + move-to-library	Skynkem123
11 — Integrator / Lead	library_manager.py main loop, JSON persistence, wiring	Theo1039
Repository: Theo1039/library-manager
Active branch: develop

🧠 Python Concepts We Learned
By building this project we got hands-on practice with:

Data structures: Lists ([]) for collections, dictionaries ({}) for book records
Control flow: for loops, while loops, if/elif/else, break, continue
Functions: def, parameters, return values, docstrings, type hints
String handling: f-strings, .strip(), .title(), .lower(), .join(), .split(), format specifiers (:.2f, :,)
User I/O: input(), print(), formatted aligned columns
Error handling: try/except for ValueError, FileNotFoundError, json.JSONDecodeError
File I/O: with open(...), JSON persistence via json.dump / json.load, CSV via the built-in csv module
Modules & imports: Splitting code across multiple files and importing them
Standard library: random.choice(), pathlib.Path, tkinter (file dialog), csv.reader/csv.writer
Collaboration: Git branches, pull requests, merge conflicts, agreeing on a shared data contract
📜 The Data Contract
Every module agrees on a single book format — the "data contract." If one module had used 'name' for title and another 'title', the app would have broken on integration day. All modules use this exact dictionary shape:

Python

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
🐛 Known Issues (pre-main checklist)
The app is fully functional — you can add, view, search, mark-read, delete, get stats, import/export, and use the wishlist without crashes on normal input. A fresh end-to-end audit (commit 54357c6) found the items below. Sorted roughly by severity. If you pick one up, tick the box and open a PR against develop.

🔴 Fix before merge (crashes / data loss)
 library_manager.py — load_library() crashes on old-format library.json.
If library.json exists but was saved by an earlier version that stored the library as a plain list (instead of {"library": [...], "wishlist": [...]}), data.get(...) on a list raises AttributeError and the app won't start. Also, if the "library" key is null, the function returns None instead of [], which crashes downstream. Add an isinstance(data, dict) guard and fall back to [] when a key is missing or null.
 csv_importer.py — Importing an exported CSV wipes read status & ratings.
csv_exporter.py writes 6 columns (title,author,year,genre,read,rating) but the importer only reads the first 4 and hardcodes read=False, rating=0 for every imported book. That means if a user exports their library and re-imports it (or shares their CSV with a friend who imports it), all reading progress and star ratings are reset to zero. Fix: detect the read/rating columns (when present) and use them; default to False/0 only when they're absent.
 csv_importer.py — No year range validation.
book_adder.py and wishlist.py both reject years outside 1000–2026, but the importer accepts any integer (-5, 3000, 999999) and then statistics will happily report it as "oldest" or "newest" book. Add the same 1000 ≤ year ≤ current-year check the other modules use.
🟡 Fix before merge (wrong / inconsistent behavior)
 wishlist.py — add_to_wishlist accepts blank author and blank genre.
book_adder.py rejects empty title/author/genre with a message and re-prompts. The wishlist only validates title, so pressing Enter on author/genre adds a book with "" for those fields. Copy the same while-loop validation pattern book_adder.py uses.
 book_marker.py — Re-marking an already-read book silently overwrites the rating.
If a book is already read=True and the user picks it again, the module sets read=True (already true) and forces a new rating, replacing the old one with no warning. Should either skip (with a message "Already read — update rating? (y/n)") or at least tell the user they're changing an existing rating.
 book_deleter.py — Confirmation only accepts exactly y/Y.
Typing yes, yeah, or y (with a trailing space) cancels the deletion instead of confirming. Accept any input whose .strip().lower() starts with y (e.g. y, Y, yes, YES).
 book_statistics.py — "Lowest rated" and average rating include 0-star (unrated) books.
When a book is marked read but hasn't been given stars yet (rating=0), min() picks it as "lowest rated" and the average gets dragged down by the zero. Filter read_books to rating > 0 before computing highest/lowest/average. If no books have ratings yet, show "No rated books yet" (already handled correctly for average — extend it to highest/lowest too).
🟢 Polish / UX (nice to have)
 book_search.py — Hitting Enter with an empty search shows every book.
Because "" in "any string" is always True in Python, a blank search matches the whole library. Ask the user to type something, or treat empty as cancel.
 Inconsistent empty-library messages. Most modules print "📭 Your library is empty! Add some books first." but book_deleter.py prints plain "There are no books to delete." and book_search.py prints "Your library is empty! Add some books first." (no emoji). Match the 📭 wording everywhere for a consistent feel.
 Hardcoded year 2026 in book_adder.py and wishlist.py. Replace with datetime.date.today().year so the app doesn't need a code change on January 1st.
 book_adder.py — Success message uses backticks (`title` by `author` has been successfully added). Plain quotes or no quotes look cleaner in a terminal.
 recommendation.py — Indentation is inconsistent (mix of 2- and 6-space indents under if not unread_books:) and one line has an extra leading space before the title. Doesn't break anything but is hard to read.
 book_display.py — Columns shift on long genre/author names. The format string uses fixed widths (:15s for genre, :16s for status), so genres longer than 15 characters push the rating column right. Consider using tabs or just a single space between sections instead of fixed-width padding.
 .title() capitalization quirk. Names entered as "CJ Archer" or "tim o'brien" get transformed by Python's .title() into "Cj Archer" and "Tim O'Brien" (the second one is fine; the first looks odd). Low priority — affects add_book and wishlist manual entry.
✅ Already fixed since the last audit
Empty title/author/genre in book_adder.py now re-prompt (while loop + continue) instead of returning to menu.
Year bug in book_adder.py (multiple commits).
book_deleter.py stray test call removed; confirmation prompt clean.
.gitignore added (ignores __pycache__/, *.pyc, etc.).
Book display wired to show after delete in the main menu.
🎉 Acknowledgements
Big thanks to the Learn2Earn fellowship coordinators for the structure and push, and to every teammate who researched a concept, wrote a module, debugged an edge case, or sat through a merge-conflict session on Integration Day. This is our first real Python app, built from scratch together.

Built with Python by beginners, for beginners.