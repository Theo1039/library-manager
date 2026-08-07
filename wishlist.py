"""
wishlist.py — Role 10: The Wishlist Keeper
--------------------------------------------
Part of the Personal Library Manager group project.

This module manages a SEPARATE list (the wishlist) of books the user
WANTS to read but doesn't own yet. It never talks to the main library
list directly except when the user explicitly asks to move a book over.

Data contract (must match every other module in the project):
    book = {
        "title": str,
        "author": str,
        "year": int,
        "genre": str,
        "read": bool,     # False by default
        "rating": int     # 0 by default (0 = unrated)
    }
"""


def add_to_wishlist(library: list, wishlist: list) -> None:
    """
    Ask the user for details about a book they want to read someday,
    and append it to the wishlist (NOT the main library).

    `library` is accepted as a parameter to match the required function
    signature from the project spec, even though this function doesn't
    use it. That keeps every module's call pattern consistent for
    Role 11 (the Integrator).
    """
    print("\n--- Add a Book to Your Wishlist ---")

    title = input("Enter book title: ").strip().title()
    if not title:
        print("❌ Title cannot be empty. Book not added.")
        return

    author = input("Enter author: ").strip().title()

    # Validate the year the same way Role 1 does, so behavior is consistent.
    year = None
    while year is None:
        year_input = input("Enter publication year: ").strip()
        try:
            year_value = int(year_input)
            if 1000 <= year_value <= 2026:
                year = year_value
            else:
                print("❌ Please enter a year between 1000 and 2026.")
        except ValueError:
            print("❌ That's not a valid number. Try again.")

    genre = input("Enter genre: ").strip().title()

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": False,
        "rating": 0,
    }

    wishlist.append(book)
    print(f"✅ '{title}' added to your wishlist!")


def view_wishlist(wishlist: list) -> None:
    """Display every book currently on the wishlist in a numbered list."""
    print("\n📋 Your Wishlist")
    print("─" * 40)

    if not wishlist:
        print("Your wishlist is empty! Add a book you're excited to read.")
        return

    for index, book in enumerate(wishlist, start=1):
        print(f"{index}. {book['title']} by {book['author']} "
              f"({book['year']}) [{book['genre']}]")


def move_to_library(library: list, wishlist: list) -> None:
    """
    Let the user pick a wishlist book by number and move it into the
    main library list. Removes it from the wishlist and appends it to
    the library, unchanged.
    """
    if not wishlist:
        print("\nYour wishlist is empty — nothing to move!")
        return

    view_wishlist(wishlist)

    choice = input(f"\nWhich book do you want to move to your library? "
                    f"(1-{len(wishlist)}), or 0 to cancel: ").strip()

    try:
        choice_num = int(choice)
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    if choice_num == 0:
        print("Cancelled.")
        return

    if not (1 <= choice_num <= len(wishlist)):
        print("❌ That number isn't on the list.")
        return

    # Convert the 1-based number the user sees to a 0-based list index.
    book = wishlist.pop(choice_num - 1)
    library.append(book)
    print(f"📚 '{book['title']}' moved to your main library!")


def wishlist_menu(library: list, wishlist: list) -> None:
    """
    Optional sub-menu that groups all three wishlist actions together.
    Role 11 can call this single function from the main menu (option 10)
    instead of wiring up three separate menu options — simpler either way.
    """
    while True:
        print("\n" + "=" * 40)
        print("    📋 WISHLIST MENU")
        print("=" * 40)
        print("1. Add a book to wishlist")
        print("2. View wishlist")
        print("3. Move a book to main library")
        print("4. Back to main menu")
        print("=" * 40)

        choice = input("Choice: ").strip()

        if choice == "1":
            add_to_wishlist(library, wishlist)
        elif choice == "2":
            view_wishlist(wishlist)
        elif choice == "3":
            move_to_library(library, wishlist)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


# Lets you run `python wishlist.py` on its own to try it out,
# without needing main.py or anyone else's code yet.
# if __name__ == "__main__":
#     library = []
#     wishlist = []
#     wishlist_menu(library, wishlist)
#     print("\nFinal library:", library)
#     print("Final wishlist:", wishlist)