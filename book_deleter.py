# Function to delete a book from the library
def delete_book(library):

    # Check if the library is empty
    if len(library) == 0:
        print("There are no books to delete.")
        return

    # Show all books with numbers
    print("\nBooks in the library:")
    for i in range(len(library)):
        book = library[i]
        print(f"{i + 1}. {book['title']} by {book['author']}")

    # Keep asking until the user enters a valid number
    while True:
        try:
            choice = int(input("\nWhich book do you want to delete? "))

            # Check if the number is valid
            if choice < 1 or choice > len(library):
                print("Invalid book number. Try again.")
            else:
                break

        except ValueError:
            print("Please enter a number only.")

    # Convert user's number to list index
    index = choice - 1
    selected_book = library[index]

    # Ask for confirmation
    confirm = input(
        f"Are you sure you want to delete '{selected_book['title']}' "
        f"by {selected_book['author']}? (y/n): "
    )

    if confirm.lower() == "y":
        library.pop(index)
        print("Book deleted successfully!")
    else:
        print("Deletion cancelled.")
