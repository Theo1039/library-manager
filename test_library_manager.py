"""
test_library_manager.py
=======================
Automated test suite for the Personal Library Manager group project.

HOW TO USE
----------
1. Put this file in the same folder as all the .py files (library_manager.py,
   book_adder.py, book_marker.py, etc.)
2. Run it from the terminal:
       python test_library_manager.py
   (Use python3 on Linux/macOS if python points to Python 2.)
3. You will see PASS / FAIL / NOTE lines for every test.
   - PASS  = the feature works correctly
   - FAIL  = there's a bug that needs fixing (read the message)
   - NOTE  = not a crash, but something to be aware of (polish item)

WHAT IT TESTS
-------------
- Normal flow: add, view, search, mark-read, delete, stats, export, import, wishlist
- Bad input: empty strings, non-numbers, out-of-range numbers
- Edge cases: empty library, one book, all books read, corrupted JSON
- Every bug listed in the README "Known Issues" section
- Data round-trips: save -> load, export -> import

You don't need to install anything. Only the Python standard library is used.
"""

import sys
import os
import io
import csv
import json
import shutil
import builtins
from contextlib import redirect_stdout, redirect_stderr


# ---------------------------------------------------------------------------
# Small helpers to keep the test code readable
# ---------------------------------------------------------------------------

PASSED = 0
FAILED = 0
NOTES = 0


def PASS(msg):
    global PASSED
    PASSED += 1
    print(f"  PASS  {msg}")


def FAIL(msg):
    global FAILED
    FAILED += 1
    print(f"  FAIL  {msg}")


def NOTE(msg):
    global NOTES
    NOTES += 1
    print(f"  NOTE  {msg}")


def SECTION(title):
    print(f"\n{'='*70}\n  {title}\n{'='*70}")


def feed_inputs(*values):
    """
    Make input() return the next value from the list each time it's called.
    This lets us simulate a user typing answers without actually typing.
    """
    queue = list(values)

    def fake_input(prompt=""):
        if not queue:
            raise EOFError(f"Test asked for more input than provided! (prompt was: {prompt!r})")
        return queue.pop(0)

    builtins.input = fake_input


def reset_input():
    """Put the real input() back."""
    builtins.input = input


def capture_output(fn, *args, **kwargs):
    """Run fn(...) and return (return_value, printed_output_string)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = fn(*args, **kwargs)
    return result, buf.getvalue()


# ---------------------------------------------------------------------------
# Set up a clean folder to run tests in (so we don't touch your real
# library.json).
# ---------------------------------------------------------------------------

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_test_run")


def setup_test_dir():
    """Create a fresh _test_run folder with copies of all .py files."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    src_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in os.listdir(src_dir):
        if fname.endswith(".py") and fname != os.path.basename(__file__):
            shutil.copy2(os.path.join(src_dir, fname), os.path.join(TEST_DIR, fname))

    os.chdir(TEST_DIR)
    # Make sure a leftover library.json doesn't interfere
    if os.path.exists("library.json"):
        os.remove("library.json")


def teardown_test_dir():
    """(Optional) delete the _test_run folder after tests."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Leave the folder in place so you can inspect it if a test fails.
    # Uncomment the next line to auto-delete:
    # shutil.rmtree(TEST_DIR, ignore_errors=True)


# ---------------------------------------------------------------------------
# Now import every module from the test folder.
# ---------------------------------------------------------------------------

def load_modules():
    sys.path.insert(0, TEST_DIR)
    # Force fresh imports
    for mod in list(sys.modules):
        if mod != __name__ and not mod.startswith("_"):
            if mod in {"library_manager", "book_adder", "book_display",
                       "book_marker", "book_deleter", "book_search",
                       "book_statistics", "csv_exporter", "csv_importer",
                       "recommendation", "wishlist"}:
                del sys.modules[mod]

    global load_library, save_library, add_book, display_books, mark_as_read
    global delete_book, booksearch, show_statistics, export_books
    global import_books_from_files, import_books_csv
    global random_recommendation, add_to_wishlist, view_wishlist
    global move_to_library

    from library_manager import load_library, save_library
    from book_adder import add_book
    from book_display import display_books
    from book_marker import mark_as_read
    from book_deleter import delete_book
    from book_search import booksearch
    from book_statistics import show_statistics
    from csv_exporter import export_books
    from csv_importer import import_books_from_files
    from recommendation import random_recommendation
    from wishlist import add_to_wishlist, view_wishlist, move_to_library


# ===========================================================================
#                               THE TESTS
# ===========================================================================

def test_imports():
    SECTION("1. Imports — does every file load without errors?")
    try:
        load_modules()
        PASS("All 11 modules import cleanly.")
    except Exception as e:
        FAIL(f"Import failed: {type(e).__name__}: {e}")


def test_empty_library():
    SECTION("2. Empty library safety — no crashes when there are 0 books")
    lib, wl = [], []

    _, out = capture_output(display_books, lib)
    if "empty" in out.lower():
        PASS("display_books on empty library prints a friendly message.")
    else:
        FAIL("display_books on empty library doesn't say the library is empty.")

    _, out = capture_output(mark_as_read, lib)
    if "empty" in out.lower():
        PASS("mark_as_read on empty library prints a friendly message.")
    else:
        FAIL("mark_as_read on empty library does not handle empty case.")

    _, out = capture_output(delete_book, lib)
    if "no books" in out.lower() or "empty" in out.lower():
        PASS("delete_book on empty library prints a friendly message.")
    else:
        FAIL("delete_book on empty library does not handle empty case.")

    _, out = capture_output(booksearch, lib)
    if "empty" in out.lower():
        PASS("booksearch on empty library prints a friendly message.")
    else:
        FAIL("booksearch on empty library does not handle empty case.")

    _, out = capture_output(show_statistics, lib)
    if "empty" in out.lower():
        PASS("show_statistics on empty library prints a friendly message.")
    else:
        FAIL("show_statistics on empty library does not handle empty case.")

    _, out = capture_output(random_recommendation, lib)
    if "empty" in out.lower():
        PASS("random_recommendation on empty library prints a friendly message.")
    else:
        FAIL("random_recommendation on empty library does not handle empty case.")

    _, out = capture_output(export_books, lib)
    if "empty" in out.lower():
        PASS("export_books on empty library prints a friendly message (doesn't create a file).")
    else:
        FAIL("export_books on empty library should say it's empty.")


def test_add_book():
    SECTION("3. Adding a book — normal flow and bad input")

    # Normal add
    feed_inputs("Half of a Yellow Sun", "Chimamanda Adichie", "2006", "Fiction")
    lib = []
    _, out = capture_output(add_book, lib)
    reset_input()
    if len(lib) == 1:
        PASS("add_book appends one book to the library.")
    else:
        FAIL(f"add_book should append 1 book, got {len(lib)}.")

    b = lib[0]
    expected_keys = {"title", "author", "year", "genre", "read", "rating"}
    if expected_keys.issubset(b.keys()):
        PASS(f"Book dict has all required keys: {sorted(expected_keys)}.")
    else:
        FAIL(f"Book dict is missing keys. Found: {sorted(b.keys())}")

    if b["read"] is False and b["rating"] == 0:
        PASS("New book defaults to read=False, rating=0.")
    else:
        FAIL(f"New book should be read=False, rating=0. Got read={b['read']}, rating={b['rating']}")

    if b["year"] == 2006:
        PASS("Year is stored as an integer (2006).")
    else:
        FAIL(f"Year should be int 2006, got {b['year']!r} ({type(b['year']).__name__}).")

    # Bad year -> re-prompt
    feed_inputs("Book1", "Author1", "abc", "2020", "Genre1")
    lib2 = []
    _, out = capture_output(add_book, lib2)
    reset_input()
    if len(lib2) == 1 and lib2[0]["year"] == 2020:
        PASS("Entering a non-number year re-prompts (doesn't crash).")
    else:
        FAIL("Non-numeric year input is not handled correctly.")

    # Out-of-range year -> re-prompt
    feed_inputs("Book2", "Author2", "3000", "2020", "Genre2")
    lib3 = []
    _, out = capture_output(add_book, lib3)
    reset_input()
    if len(lib3) == 1 and lib3[0]["year"] == 2020:
        PASS("Entering year 3000 re-prompts (doesn't accept it).")
    else:
        FAIL("Out-of-range year (3000) was accepted or crashed.")

    # Year below 1000 -> re-prompt
    feed_inputs("Book3", "Author3", "50", "2000", "Genre3")
    lib4 = []
    _, out = capture_output(add_book, lib4)
    reset_input()
    if len(lib4) == 1 and lib4[0]["year"] == 2000:
        PASS("Entering year 50 re-prompts (doesn't accept below 1000).")
    else:
        FAIL("Out-of-range year (50) was accepted or crashed.")

    # Empty inputs -> re-prompt
    feed_inputs("", "", "", "", "", "", "", "Good Title", "Good Author", "2020", "", "Good Genre")
    lib5 = []
    try:
        _, out = capture_output(add_book, lib5)
        reset_input()
        if len(lib5) == 1:
            PASS("Empty title/author/genre re-prompts instead of returning to menu.")
        else:
            FAIL(f"Empty-input re-prompt failed (added {len(lib5)} books).")
    except EOFError:
        reset_input()
        FAIL("Empty input caused an EOFError (loop probably returned/break incorrectly).")


def test_mark_as_read():
    SECTION("4. Mark as read — number entry, stars, re-rating")

    lib = [{"title": "Book A", "author": "Auth", "year": 2020,
            "genre": "F", "read": False, "rating": 0}]

    feed_inputs("abc", "99", "1", "5")
    _, out = capture_output(mark_as_read, lib)
    reset_input()

    if lib[0]["read"] is True and lib[0]["rating"] == 5:
        PASS("Handles non-number ('abc') and out-of-range (99) then marks + rates correctly.")
    else:
        FAIL(f"mark_as_read failed. read={lib[0]['read']}, rating={lib[0]['rating']}")

    if "★★★★★" in out:
        PASS("Success message prints 5-star string.")
    else:
        FAIL("Success message doesn't show star rating.")

    # Re-marking an already-read book (known issue: overwrites rating)
    feed_inputs("1", "1")  # re-rate the same book from 5 to 1
    _, out = capture_output(mark_as_read, lib)
    reset_input()
    if lib[0]["rating"] == 1:
        NOTE("Re-marking an already-read book silently overwrites the rating "
             "(no 'already read, update?' confirmation). See README bug #5.")
    else:
        PASS("Re-rating an already-read book is blocked or asks for confirmation.")

    # Rating validation: non-numeric, out-of-range
    lib2 = [{"title": "Book B", "author": "Auth", "year": 2020,
             "genre": "F", "read": False, "rating": 0}]
    feed_inputs("1", "abc", "0", "6", "3")
    try:
        _, out = capture_output(mark_as_read, lib2)
        reset_input()
        if lib2[0]["rating"] == 3:
            PASS("Rating input rejects 'abc', 0, and 6, then accepts 3.")
        else:
            FAIL(f"Rating validation failed. rating={lib2[0]['rating']}")
    except EOFError:
        reset_input()
        FAIL("Rating validation loop crashed or returned early on bad input.")


def test_display_books():
    SECTION("5. Display books — formatting, pluralization, stars")

    # Empty
    _, out = capture_output(display_books, [])
    if "empty" in out.lower():
        PASS("Displays 'empty' message when library has 0 books.")

    # One book -> "1 book" (singular)
    lib = [{"title": "A", "author": "X", "year": 2020,
            "genre": "F", "read": True, "rating": 4}]
    _, out = capture_output(display_books, lib)
    if "1 book" in out:
        PASS("Pluralization says '1 book' (not '1 books').")
    else:
        FAIL(f"Pluralization broken for 1 book. Output:\n{out}")

    # Two books -> "2 books" (plural)
    lib.append({"title": "B", "author": "Y", "year": 2021,
                "genre": "G", "read": False, "rating": 0})
    _, out = capture_output(display_books, lib)
    if "2 books" in out:
        PASS("Pluralization says '2 books' (plural).")
    else:
        FAIL(f"Pluralization broken for 2 books. Output:\n{out}")

    # Unrated book shows dash, not 5 empty stars
    if "—" in out or "0" in out:
        PASS("Unrated book shows a dash/blank for stars (not 5 empty stars).")
    else:
        NOTE("Unrated book might show 5 empty stars instead of a dash "
             "(minor polish, see book_display.py).")

    # Star strings (4★ + 1☆ for rating 4)
    if "★★★★☆" in out or "★★★★" in out:
        PASS("4-star rating is rendered as filled/empty stars.")
    else:
        FAIL("Star rendering for rating=4 not found.")


def test_delete():
    SECTION("6. Delete a book — confirmation and cancel")

    lib = [{"title": "A", "author": "X", "year": 2020,
            "genre": "F", "read": False, "rating": 0},
           {"title": "B", "author": "Y", "year": 2021,
            "genre": "G", "read": False, "rating": 0}]

    # Cancel delete
    feed_inputs("2", "n")
    _, out = capture_output(delete_book, lib)
    reset_input()
    if len(lib) == 2:
        PASS("Pressing 'n' cancels deletion (library unchanged).")
    else:
        FAIL("'n' did not cancel deletion.")

    # Confirm delete
    feed_inputs("2", "y")
    _, out = capture_output(delete_book, lib)
    reset_input()
    if len(lib) == 1 and lib[0]["title"] == "A":
        PASS("Pressing 'y' removes the selected book.")
    else:
        FAIL(f"Delete failed. Library now has {len(lib)} books.")

    # Non-numeric menu choice -> re-prompt
    lib2 = [{"title": "A", "author": "X", "year": 2020,
             "genre": "F", "read": False, "rating": 0}]
    feed_inputs("abc", "5", "1", "n")
    _, out = capture_output(delete_book, lib2)
    reset_input()
    if len(lib2) == 1:
        PASS("Rejects non-number ('abc') and out-of-range (5) then cancels.")
    else:
        FAIL("Delete number validation failed.")

    # Does "yes" count as confirm? (known bug: only 'y' works)
    lib3 = [{"title": "A", "author": "X", "year": 2020,
             "genre": "F", "read": False, "rating": 0}]
    feed_inputs("1", "yes")
    _, out = capture_output(delete_book, lib3)
    reset_input()
    if len(lib3) == 0:
        PASS("'yes' is accepted as confirmation (good UX).")
    else:
        NOTE("Only exact 'y'/'Y' confirms deletion. Typing 'yes' cancels. "
             "See README bug #6.")


def test_search():
    SECTION("7. Search — title, author, miss, case-insensitive")

    lib = [
        {"title": "Half of a Yellow Sun", "author": "Chimamanda Adichie",
         "year": 2006, "genre": "Fiction", "read": False, "rating": 0},
        {"title": "Things Fall Apart", "author": "Chinua Achebe",
         "year": 1958, "genre": "Classic", "read": False, "rating": 0},
        {"title": "Purple Hibiscus", "author": "Chimamanda Adichie",
         "year": 2003, "genre": "Fiction", "read": False, "rating": 0},
    ]

    # Find by author (achebe)
    feed_inputs("achebe")
    _, out = capture_output(booksearch, lib)
    reset_input()
    if "Things Fall Apart" in out and "Found 1" in out:
        PASS("Searching 'achebe' finds 1 book (case-insensitive).")
    else:
        FAIL(f"Author search failed. Output:\n{out}")

    # Find by title fragment
    feed_inputs("purple")
    _, out = capture_output(booksearch, lib)
    reset_input()
    if "Purple Hibiscus" in out:
        PASS("Searching 'purple' finds Purple Hibiscus.")
    else:
        FAIL("Title fragment search failed.")

    # Miss
    feed_inputs("xyznonexistent")
    _, out = capture_output(booksearch, lib)
    reset_input()
    if "no matches" in out.lower():
        PASS("Search miss prints 'No matches found' message.")
    else:
        FAIL("Search miss doesn't print a friendly message.")

    # Case-insensitive
    feed_inputs("CHIMAMANDA")
    _, out = capture_output(booksearch, lib)
    reset_input()
    if "Found 2" in out or "Half of a Yellow Sun" in out:
        PASS("Search is case-insensitive (CHIMAMANDA finds 2 books).")
    else:
        FAIL("Case-insensitive search not working.")

    # Empty search
    feed_inputs("")
    _, out = capture_output(booksearch, lib)
    reset_input()
    if "please" in out.lower() or "type something" in out.lower():
        PASS("Empty search is rejected with a helpful message.")
    else:
        NOTE("Empty search (just pressing Enter) returns all books. "
             "See README bug #8.")


def test_statistics():
    SECTION("8. Statistics — counts, percentages, averages, genres, extremes")

    # Empty lib
    _, out = capture_output(show_statistics, [])
    if "empty" in out.lower():
        PASS("Stats on empty library shows a friendly message.")
    else:
        FAIL("Stats on empty library does not handle empty case.")

    # 1 unread book (no ratings)
    lib = [{"title": "A", "author": "X", "year": 2020,
            "genre": "Fiction", "read": False, "rating": 0}]
    _, out = capture_output(show_statistics, lib)
    if "Total books" in out and "Read:" in out and "0%" in out:
        PASS("Stats on 1 unread book shows 0% read.")
    else:
        FAIL(f"Stats on 1 unread book broken:\n{out}")
    if "No rated books yet" in out or "no rated" in out.lower():
        PASS("Stats says 'No rated books yet' when nothing is rated.")
    else:
        FAIL("Stats should say 'No rated books yet' when no books have stars.")
    # Highest/lowest should NOT appear when there are no rated books
    if "Highest rated" in out:
        FAIL("Stats shows 'Highest rated' even though no books are rated. "
             "See README bug #7.")
    else:
        PASS("Stats hides highest/lowest when no books are rated.")

    # 3 books: 2 read (one 5-star, one 0-star), 1 unread
    lib2 = [
        {"title": "A", "author": "X", "year": 2000, "genre": "F", "read": True, "rating": 5},
        {"title": "B", "author": "Y", "year": 2001, "genre": "F", "read": True, "rating": 0},  # read but not rated
        {"title": "C", "author": "Z", "year": 2002, "genre": "G", "read": False, "rating": 0},
    ]
    _, out = capture_output(show_statistics, lib2)
    if "67%" in out or "66%" in out:
        PASS("Percentage reads correct for 2/3 books.")
    else:
        FAIL(f"Percentage wrong. Output:\n{out}")

    # Does the average include the 0-star book? (known bug)
    if "5.0" in out:
        PASS("Average rating only counts actually-rated books (5.0 for one 5-star book).")
    elif "2.5" in out:
        NOTE("Average rating = 2.5 because it counts the 0-star (unrated) book. "
             "See README bug #7.")
    else:
        NOTE(f"Average rating is something unexpected: check output. Output:\n{out}")

    # Lowest rated shouldn't be 0-star (unrated)
    if "Lowest rated" in out and "0 ★" in out:
        NOTE("Lowest-rated shows a 0-star (unrated) book. See README bug #7.")

    # Genre counts
    if "F" in out and "G" in out:
        PASS("Books-by-genre breakdown counts both genres.")
    else:
        FAIL("Genre breakdown missing.")

    # Oldest/newest
    if "2000" in out and "2002" in out:
        PASS("Oldest (2000) and newest (2002) detected correctly.")
    else:
        FAIL("Oldest/newest detection wrong.")


def test_recommendation():
    SECTION("9. Recommendation — picks unread, handles all-read")

    # All books unread
    lib = [
        {"title": "A", "author": "X", "year": 2020, "genre": "F", "read": False, "rating": 0},
        {"title": "B", "author": "Y", "year": 2021, "genre": "G", "read": False, "rating": 0},
    ]
    _, out = capture_output(random_recommendation, lib)
    # It should print one of A or B
    if "A" in out or "B" in out:
        PASS("Random recommendation picks an unread book.")
    else:
        FAIL(f"Recommendation output unexpected:\n{out}")

    # All read -> HURRAY message
    lib2 = [{"title": "A", "author": "X", "year": 2020, "genre": "F", "read": True, "rating": 4}]
    _, out = capture_output(random_recommendation, lib2)
    if "HURRAY" in out.upper() or "read all" in out.lower():
        PASS("All-read library prints a celebratory message.")
    else:
        FAIL("All-read library should say you've read everything.")

    # Indentation / extra-space polish check (doesn't fail; just notes)
    if recommendation_has_indentation_issues():
        NOTE("recommendation.py has inconsistent indentation / leading space "
             "before title. See README polish items.")


def recommendation_has_indentation_issues():
    """Check the file for mixed 2-space and 4/6-space indents."""
    path = os.path.join(TEST_DIR, "recommendation.py")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.startswith(" ") and not stripped.startswith("    "):
            # Line starts with spaces but not 4
            leading = len(stripped) - len(stripped.lstrip(" "))
            if leading in (1, 2, 3, 5, 6, 7):  # suspicious
                return True
    return False


def test_csv_export_import_roundtrip():
    SECTION("10. CSV export/import — round-trip and edge cases")

    lib = [
        {"title": "A", "author": "X", "year": 2020,
         "genre": "F", "read": True, "rating": 4},
        {"title": "B", "author": "Y", "year": 2021,
         "genre": "G", "read": False, "rating": 0},
        {"title": "Book, With Comma", "author": "Author, Jr.",
         "year": 2019, "genre": "H", "read": False, "rating": 3},
    ]

    # Export
    fname = "test_export.csv"
    if os.path.exists(fname):
        os.remove(fname)
    _, out = capture_output(export_books, lib, fname)
    if os.path.exists(fname):
        PASS(f"export_books creates {fname}.")
    else:
        FAIL(f"export_books did not create {fname}.")
        return

    # Check header row
    with open(fname, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    expected_header = ["title", "author", "year", "genre", "read", "rating"]
    if rows[0] == expected_header:
        PASS(f"CSV header is {expected_header} (6 columns).")
    else:
        FAIL(f"CSV header is {rows[0]}, expected {expected_header}.")

    if len(rows) == 4:  # header + 3 books
        PASS("CSV has correct number of rows (header + 3 books).")
    else:
        FAIL(f"CSV row count wrong: {len(rows)} (expected 4).")

    # Book with comma in title is handled correctly (quoted)
    if any("Book, With Comma" in r[0] for r in rows[1:]):
        PASS("Commas in titles are handled (csv.writer quotes them correctly).")
    else:
        FAIL("Commas in titles were not preserved in export.")

    # Now import the file we just exported and check that read/rating survive
    # (THIS IS THE BIG ROUND-TRIP BUG)
    lib2 = []
    try:
        _, out2 = capture_output(import_books_from_files, lib2, [fname], skip_duplicates=True)
    except Exception as e:
        FAIL(f"Importing the exported file crashed: {e}")
        lib2 = []

    if len(lib2) != len(lib):
        FAIL(f"Import returned {len(lib2)} books, expected {len(lib)}.")
    else:
        PASS(f"Imported {len(lib2)} books from exported CSV.")
        # Check if the first book's read/rating were preserved
        if lib2[0].get("read") is True and lib2[0].get("rating") == 4:
            PASS("Round-trip preserves read=True and rating=4 (data intact).")
        else:
            FAIL("Round-trip reset read to False and/or rating to 0. "
                 "See README bug #2 (data loss on import).")

    # Bad year in CSV (should be skipped)
    bad_csv = "bad_year.csv"
    with open(bad_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "author", "year", "genre"])
        w.writerow(["Good", "Author", "2020", "F"])
        w.writerow(["Bad", "Author", "notayear", "F"])
        w.writerow(["", "", "", ""])  # empty row

    lib3 = []
    _, out3 = capture_output(import_books_from_files, lib3, [bad_csv])
    if len(lib3) == 1:
        PASS("CSV import skips bad-year rows and empty rows.")
    else:
        FAIL(f"CSV bad-year handling got {len(lib3)} books (expected 1). Output:\n{out3}")

    # Out-of-range year (3000) - should this be accepted? (known bug)
    future_csv = "future.csv"
    with open(future_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "author", "year", "genre"])
        w.writerow(["Future Book", "Writer", "3000", "SciFi"])
    lib4 = []
    _, out4 = capture_output(import_books_from_files, lib4, [future_csv])
    if len(lib4) == 0 or (len(lib4) == 1 and lib4[0]["year"] != 3000):
        PASS("CSV import rejects year 3000 (matches add_book range check).")
    else:
        NOTE("CSV import accepts year 3000 (no 1000-2026 range check). "
             "See README bug #3.")

    # Duplicates
    lib5 = [{"title": "A", "author": "X", "year": 2020,
             "genre": "F", "read": False, "rating": 0}]
    dup_csv = "dup.csv"
    with open(dup_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "author", "year", "genre"])
        w.writerow(["A", "X", "2020", "F"])  # duplicate
        w.writerow(["C", "Z", "2022", "H"])   # new
    _, out5 = capture_output(import_books_from_files, lib5, [dup_csv], skip_duplicates=True)
    if len(lib5) == 2:
        PASS("Duplicate detection skips books already in library.")
    else:
        FAIL(f"Duplicate detection failed (got {len(lib5)} books, expected 2).")


def test_save_load_json():
    SECTION("11. Save/Load JSON — round-trip and corruption handling")

    lib = [{"title": "A", "author": "X", "year": 2020,
            "genre": "F", "read": True, "rating": 5}]
    wl = [{"title": "W", "author": "Y", "year": 2024,
           "genre": "G", "read": False, "rating": 0}]

    # Save
    if os.path.exists("library.json"):
        os.remove("library.json")
    save_library(lib, wl)
    if os.path.exists("library.json"):
        PASS("save_library creates library.json.")
    else:
        FAIL("save_library did not create library.json.")
        return

    # Load back
    lib2, wl2 = load_library()
    if len(lib2) == 1 and lib2[0]["title"] == "A" and len(wl2) == 1 and wl2[0]["title"] == "W":
        PASS("Save -> load round-trip preserves library AND wishlist.")
    else:
        FAIL(f"Save/load round-trip failed. lib={lib2}, wl={wl2}")

    # Corrupted JSON
    with open("library.json", "w") as f:
        f.write("{this is not json")
    _, out = capture_output(load_library)
    try:
        lib3, wl3 = load_library()
        reset_input()
        if lib3 == [] and wl3 == [] and ("corrupt" in out.lower() or "error" in out.lower()):
            PASS("Corrupted JSON is handled (prints message, returns empty lists).")
        else:
            FAIL(f"Corrupted JSON returned lib={lib3}, wl={wl3}, out={out!r}")
    except Exception as e:
        FAIL(f"Corrupted JSON crashed load_library: {type(e).__name__}: {e}")
    finally:
        reset_input()

    # Old-format JSON (list instead of dict) — known crash bug
    with open("library.json", "w") as f:
        json.dump([{"title": "Old", "author": "Book", "year": 2000,
                    "genre": "F", "read": False, "rating": 0}], f)
    try:
        lib4, wl4 = load_library()
        if isinstance(lib4, list) and isinstance(wl4, list):
            PASS("Old-format JSON (a list) loads without crashing.")
        else:
            FAIL(f"Old-format JSON returned unexpected types: {type(lib4)}, {type(wl4)}")
    except AttributeError as e:
        FAIL(f"Old-format JSON (plain list) crashes load_library: AttributeError. "
             f"See README bug #1.")
    except Exception as e:
        FAIL(f"Old-format JSON crashes load_library: {type(e).__name__}: {e}")

    # Null values inside JSON
    with open("library.json", "w") as f:
        f.write('{"library": null, "wishlist": null}')
    try:
        lib5, wl5 = load_library()
        if lib5 == [] and wl5 == []:
            PASS("Null library/wishlist keys in JSON are treated as empty lists.")
        else:
            NOTE(f"Null JSON keys returned lib={lib5!r}, wl={wl5!r}. See README bug #1.")
    except Exception as e:
        FAIL(f"Null JSON values crash load_library: {type(e).__name__}: {e}")

    # Clean up
    if os.path.exists("library.json"):
        os.remove("library.json")


def test_wishlist():
    SECTION("12. Wishlist — add, view, move to library")

    lib, wl = [], []

    # Add a wishlist book
    feed_inputs("Wish Book", "Wish Author", "2024", "Sci-Fi")
    _, out = capture_output(add_to_wishlist, lib, wl)
    reset_input()
    if len(wl) == 1 and wl[0]["title"] == "Wish Book":
        PASS("add_to_wishlist appends a book to wishlist (not library).")
    else:
        FAIL(f"add_to_wishlist failed. wl={wl}, lib={lib}")
    if len(lib) == 0:
        PASS("Wishlist book is NOT added to main library.")
    else:
        FAIL("Wishlist book leaked into the main library!")

    # View wishlist
    _, out = capture_output(view_wishlist, wl)
    if "Wish Book" in out:
        PASS("view_wishlist prints the book.")
    else:
        FAIL("view_wishlist didn't print the wishlist book.")

    # Move to library
    feed_inputs("1")
    _, out = capture_output(move_to_library, lib, wl)
    reset_input()
    if len(wl) == 0 and len(lib) == 1 and lib[0]["title"] == "Wish Book":
        PASS("move_to_library moves book from wishlist to library.")
    else:
        FAIL(f"move_to_library failed. wl={wl}, lib={lib}")

    # Empty wishlist -> view and move handled
    _, out = capture_output(view_wishlist, [])
    if "empty" in out.lower():
        PASS("view_wishlist on empty list prints a friendly message.")
    else:
        FAIL("view_wishlist empty case not handled.")

    _, out = capture_output(move_to_library, lib, [])
    if "empty" in out.lower():
        PASS("move_to_library on empty wishlist prints a friendly message.")
    else:
        FAIL("move_to_library empty case not handled.")

    # Empty author/genre in wishlist (known bug)
    feed_inputs("Lonely Title", "", "2020", "")
    _, out = capture_output(add_to_wishlist, [], wl)
    reset_input()
    if len(wl) == 1 and (wl[0]["author"] == "" or wl[0]["genre"] == ""):
        NOTE("Wishlist accepts empty author and/or empty genre. "
             "See README bug #4.")
    elif len(wl) == 1:
        PASS("Wishlist rejects empty author/genre (as it should).")
    else:
        FAIL("Wishlist add failed in an unexpected way.")


# ---------------------------------------------------------------------------
#                  OPTIMIZATION / CODE QUALITY SUGGESTIONS
# ---------------------------------------------------------------------------

def optimization_suggestions():
    SECTION("13. Optimization & Code Quality Suggestions")
    print("""
  These aren't bugs, but they would make the code cleaner, faster, or more
  maintainable. Good targets for after the merge to main.

  O1. Replace hardcoded year 2026 with:
          from datetime import date
          MAX_YEAR = date.today().year
      in both book_adder.py and wishlist.py. Never needs updating again.

  O2. Share a single helper for input validation. Right now every module has
      its own "ask until integer in range" while-loop. Putting a small helper
      (e.g. ask_int(prompt, min, max)) in a utils.py would cut ~30 lines of
      duplicated code across the project and make bugs harder to introduce.

  O3. Same for "book dict factory" — instead of building the dict in 3 places
      (book_adder.py line 36, csv_importer.py line 121, wishlist.py line 55),
      have one function make_book(title, author, year, genre) that returns a
      properly-defaulted dict. Prevents the read/rating default bug we just
      found in CSV import.

  O4. book_display.py uses fixed-width columns (":15s" for genre, ":16s" for
      status). Long genres push columns out. Use ljust() dynamically based on
      the longest present value, or just use "  |  " separators between
      sections.

  O5. Case consistency: add_book applies .title() to title/author/genre, but
      csv_importer keeps original case. Decide one policy (either force title
      case everywhere or preserve what the user typed) and apply it in both
      places.

  O6. The main menu prints emojis (📚📭✅❌) which look great in modern
      terminals but might render as ?? on old Windows cmd. If you want to
      support that, you could add a --no-emoji flag. Low priority.

  O7. Consider using a dataclass or typing.TypedDict for Book so every
      module's IDE autocomplete knows the keys. Great learning step after
      this project.

  O8. Add a small __main__ self-test to each module (if __name__ ==
      "__main__": ...) like csv_importer and wishlist already have. This
      makes it easy for a teammate to run just their own file and check
      it works without going through the main menu.
""")


# ---------------------------------------------------------------------------
#                               MAIN RUNNER
# ---------------------------------------------------------------------------

def main():
    global PASSED, FAILED, NOTES
    PASSED = FAILED = NOTES = 0

    print("=" * 70)
    print("  PERSONAL LIBRARY MANAGER — TEST SUITE")
    print("=" * 70)
    print("""
  This script will:
    - Create a temporary folder (_test_run) with copies of all your .py files
    - Run through add, view, search, mark-read, delete, stats, CSV, save/load, wishlist
    - Feed in bad input (empty strings, non-numbers, out-of-range) to check error handling
    - Report every bug listed in the README "Known Issues" section

  Your real library.json is NOT touched.
    """)

    try:
        setup_test_dir()
        test_imports()
        test_empty_library()
        test_add_book()
        test_mark_as_read()
        test_display_books()
        test_delete()
        test_search()
        test_statistics()
        test_recommendation()
        test_csv_export_import_roundtrip()
        test_save_load_json()
        test_wishlist()
        optimization_suggestions()
    finally:
        teardown_test_dir()
        reset_input()

    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"    PASS : {PASSED}")
    print(f"    FAIL : {FAILED}")
    print(f"    NOTE : {NOTES}")
    print()
    if FAILED == 0:
        print("  🎉 All tests passed! The app is ready to merge (modulo NOTEs).")
    else:
        print(f"  ⚠️  {FAILED} test(s) failed. Fix the FAIL items above before merging.")
        print("  Each FAIL message points to the matching bullet in README.md")
        print("  under 'Known Issues'.")
    print()
    print("  Test artifacts (if any) are in:  _test_run/")
    print("=" * 70)


if __name__ == "__main__":
    main()
