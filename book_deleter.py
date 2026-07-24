
# function to delete a book from the library
def delete_book(library: list) -> None:
    
    #check if the library is empty
    if len(library) == 0:
        print("There are no books to delete.")
        return
    
    # show all books with numbers
    print("\nBooks in the library:")
    for i in range(len(library)):
          print(f"{i + 1}.{library[i]}")
    
    # keep asking until the user enters a valid number
    while True:
        try:
            choice = int(input("\nwhich book do you want to delete? "))
            
            # check if the number is valid
            if choice < 1 or choice > len(library):
                print("Invalid book number. Try again.")
            else: 
                break

        except ValueError:
            print("Please enter a number only.")

        # convert users number to list index
    index = choice - 1   
        
        # Ask for confirmation
    confirm = input(f"Are you sure you want to delete'{library[index]}'? (y/n): ")

    if confirm.lower() == "y":
           deleted_book = library.pop(index)
           print(f"'{deleted_book}' has been deleted successfully!")
    elif confirm == "n":
            print("Deletion cancelled.")
    else:
         print("invalid input. Please enter only 'y' or 'n'.")

         
delete_book(library)

    #show updated library
print("\nUpdated Library:")
for book in library:
        print("_", book)
