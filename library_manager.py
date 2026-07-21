import json
from book_adder import add_book

Library_file = "library.json" # this acts as storage for library data (library and wishlist)


def load_library()-> tuple[list, list]:
    """Load the library from a JSON file. Return empty list if file doesn't exist."""
    # TODO: Use try/except to open LIBRARY_FILE and return json.load(file)
    # If FileNotFoundError, return []

    try:
        with open(Library_file, "r") as file:
            data = json.load(file)
            #Assuming we saved them as a dictionary containing both lists (library and wishlist)
            return data.get("library", []), data.get("wishlist", [])
            #get used here search for the "library" key and also "wishlist" key, if not found it returns an empty list []
    except FileNotFoundError:
        # if Library_file cannot be found return two empty list
        return [], []


def save_library(library: list, wishlist: list) -> None:
    """Save the library list to a JSON file."""
    # TODO: Open LIBRARY_FILE in 'w' mode and use json.dump(library, file, indent=2)
    save_data = {
        "library": library,
        "wishlist": wishlist
    }
    
    with open(Library_file, "w") as file:
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
    print("8. Import book books from a CSV")
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
            search_books(library)
        elif choice == "4":
            mark_as_read(library)
        elif choice == "5":
            delete_book(library)
        elif choice == "6":
            show_statistics(library)
        elif choice == "7":
            random_recommendation(library)
        elif choice == "8":
            import_books(library)
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
