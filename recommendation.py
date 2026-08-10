# Book recommendation
import random
#Define a random recommendation
def random_recommendation(library: list)-> None:
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

#Recomments a random book to the user
    Recommendation = random.choice(unread_books)

    print(f" {Recommendation['title']} by"
          f" {Recommendation['author']} ({Recommendation['year']})")

    print("Give this a try")


# library = [{"title": "Dune",
#        "author": "Frank Herbert",
#        "year": 1965,
#        "Genre": "fiction",
#        "read": False
#          },
#        {
#         "title": "Atomic Habits",
#          "author": "James Clear",
#           "year": 2018,
#           "Genre": "fiction",
#          "read": True

#         },
#         {
#          "title": "The Hobbit",
#            "author": "J.R.R.Tolkien",
#             "year": 1937,
#             "Genre": "fiction",
#              "read": False
#         }
# ]
# random_recommendation(library)                #integrated already, no need calling it here



