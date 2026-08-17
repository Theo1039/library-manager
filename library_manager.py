import json
from book_adder import add_book
from book_deleter import delete_book
from book_marker import mark_as_read
from csv_exporter import export_books
from csv_importer import import_books_csv
from book_search import booksearch
from book_statistics import show_statistics
from wishlist import wishlist_menu
from recommendation import random_recommendation
from book_display import display_books

LIBRARY_FILE = "library.json" # this acts as storage for library data (library and wishlist)


def load_library()-> tuple[list, list]:
    """Load the library from a JSON file. Return empty list if file doesn't exist."""

    try:
        with open(LIBRARY_FILE, "r") as file:
            data = json.load(file)
            #Assuming we saved them as a dictionary containing both lists (library and wishlist)
            #get used here search for the "library" key and also "wishlist" key, if not found it returns an empty list []
    except FileNotFoundError:
        # if Library_file cannot be found return two empty list
        return [], []
    except json.JSONDecodeError:
        print("Library.json is corrupted - starting fresh.")
        return [],[]

    # Old format (before wishlist existed): file was just a plain list of books
    if isinstance(data, list):
        return data, []

    #Normal format: {"library": [...], "wishlist": [...]}
    #Guard against null / missing keys by using 'or []'
    library = data.get("library") or []
    wishlist = data.get("wishlist") or []

    #Extra safety: if a key is present but is not a list (corruption),
    #don't let it crash downstream - start fresh for that list.
    if not isinstance(library, list):
        library = []
    if not isinstance(wishlist, list):
        wishlist = []

    return library, wishlist


def save_library(library: list, wishlist: list) -> None:
    """Save the library list to a JSON file."""
    save_data = {
        "library": library,
        "wishlist": wishlist
    }
    
    with open(LIBRARY_FILE, "w") as file:
        #json.dump saves the current state of the library and wishlist to library_file
        json.dump(save_data, file, indent=4)


def print_menu():
    print("\n" + "=" * 40)
    print("    📚 PERSONAL LIBRARY MANAGER")
    print("=" * 40)
    print("1. Add a Book")
    print("2. View All Books")
    print("3. Search Books")
    print("4. Mark a Book as Read")
    print("5. Delete a Book")
    print("6. Show Statistics")
    print("7. Random Recommendation")
    print("8. Import book(s) from a CSV")
    print("9. Export library to CSV")
    print("10. View reading wishlist")
    print("11. Save & Exit")
    print("=" * 40)


def main():
    library, wishlist = load_library()

    while True:
        print_menu()
        choice = input("Enter your choice (1-11): ").strip()
        # strip() takes away any whitespaces (spaces, tabs, newlines) from the users input

        if choice == "1":
            add_book(library)
        elif choice == "2":
            display_books(library)
        elif choice == "3":
            booksearch(library)
        elif choice == "4":
            mark_as_read(library)
        elif choice == "5":
            delete_book(library)
            print("\nUpdated Library:")
            display_books(library)              # updated library is displayed
        elif choice == "6":
            show_statistics(library)
        elif choice == "7":
            random_recommendation(library)
        elif choice == "8":
            import_books_csv(library)
        elif choice == "9":
            export_books(library)
        elif choice == "10":
            wishlist_menu(library, wishlist)
        elif choice == "11":
            save_library(library, wishlist)
            print("✅ Library saved! Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number 1-11.")


if __name__ == "__main__":
    main()
