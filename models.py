# class Book:
#   # Class property: accessible via Book.id or Book.book_list
#   id = 1
#   book_list = []
#   # Every book should have title,author,id
#   def __init__(self,title,author):
#     self.title = title
#     self.author = author
#     self.id = Book.id
#     # update 'book_list' class property
#     Book.book_list.append(self)
#     # increment id
#     Book.id += 1

#   @classmethod
#   # With 'classmethod' decorator, first parameter is always the class in which function resides
#   # It is implicitly passed as a parameter, so only additional params ('id') need to be
#   # explicitly passed
#   def find(cls, id):
#     return [book for book in cls.book_list if book.id == id][0]