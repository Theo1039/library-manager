
# function to delete a book from the library
def delete_book(library):
    
    #check if the library is empty
    if len(library) == 0:
        print("There are no books to delete.")
        return
    
    # show all books with numbers
    print("\nBooks in the library:")
    for i in range(len(library)):
          book = library[i]
          print(f"{i + 1}.{book['title']} by {book['author']}")#changed "tittle" to "title"
    
    # keep asking until the user enters a valid number
    while True:
        try:
            choice = int(input("\nwhich book do you want to delete? "))
            
            # check if the number is valid
            if choice < 1 or choice > len(library):
                print("Invalid book number. Try again.")
            else: break

        except ValueError:
            print("Please enter a number only.")

    # convert users number to list index
    index = choice - 1   
        
    # Ask for confirmation
    confirm = input(f"Are you sure you want to delete {library[index]['title']}? (y/n): ")  #fix: correct raw dictionary string print in delete_book confirmation prompt

    if confirm.lower() == "y":
           library.pop(index)
           print("Book deleted successfully!")
    else:
            print("Deletion cancelled.")

# Example library
# library = []

    # call the function
# delete_book(library)              # no need the call the function at this point after integration

    #show updated library
# print("\nUpdated Library:")       # called display_book() in library_manager.py instead
# for book in library:
#         print("_", book)
