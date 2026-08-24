# Book recommendation
import random
#Define a random recommendation
def random_recommendation(library: list)-> None:
    if len(library) == 0:
        print("📭 Your library is empty! Add some books first.")
        return
    unread_books =[]
# makes a list of unread books
    for book in library:
        if not book["read"]:
            unread_books.append(book)

# checks if the user had read all the books
    if not unread_books:
      print("HURRAY !!!!")
      print("You have read all the books in your library")
      print("You can now add more books to your library")
      return

#recommends a random book to the user
    recommended_book = random.choice(unread_books)
    print(f" {recommended_book['title']} by"
        f" {recommended_book['author']} ({recommended_book['year']})")
    print("Give this a try")
