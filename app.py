from flask import Flask, render_template, redirect, request, url_for
# Flask - class used to initialize an app
# render_template - render a template
# request - getting form data via POST request
# redirect - respond with location header
# url_for - shorthand for using function name instead
  # of name of route

from flask_sqlalchemy import SQLAlchemy

from flask_modus import Modus
# Modus - allows us to do method override
  # via headers 'X-HTTP-method-override' 
  # or query string with '?_method'

# from models import Book

class Book:
  # Class property: accessible via Book.id or Book.book_list
  id = 1
  book_list = []
  # Every book should have title,author,id
  def __init__(self,title,author):
    self.title = title
    self.author = author
    self.id = Book.id
    # update 'book_list' class property
    Book.book_list.append(self)
    # increment id
    Book.id += 1

  @classmethod
  # With 'classmethod' decorator, first parameter is always the class in which function resides
  # It is implicitly passed as a parameter, so only additional params ('id') need to be
  # explicitly passed
  def find(cls, id):
    return [book for book in cls.book_list if book.id == id][0]

# Seed some dummy data
Book('Gatsby', 'Fitzy')

# create 'app' module by passing __name__ to Flask class
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/sqlalchemy_app'
db = SQLAlchemy(app)

# create module ('modus') by passing 'app' to class ('Modus')
modus = Modus(app)


# Decorator is a function that will add some additional
# functionality to the function it is passed to,
# and then return a function (but not invoke it)

@app.route('/')
def root():
  return redirect(url_for('index'))

@app.route('/books')
def index():
  return render_template('index.html', books=Book.book_list)

# NEW
@app.route('/books/new')
def new():
  return render_template('new.html')

# SHOW
@app.route('/books/<int:id>')
def show(id):
  return render_template('show.html', book=Book.find(id))

# EDIT
@app.route('/books/<int:id>/edit')
def edit(id):
  return render_template('edit.html', book=Book.find(id))

# CREATE
@app.route('/books', methods = ['POST'])
def create():
  Book(request.form['title'], request.form['author'])
  return redirect(url_for('index'))

# UPDATE
@app.route('/books/<int:id>', methods = ['PATCH'])
def update(id):
  found_book = Book.find(id)
  found_book.title = request.form['title']
  found_book.author = request.form['author']
  return redirect(url_for('index'))

# DELETE
@app.route('/books/<int:id>', methods = ['DELETE'])
def destroy(id):
  found_book = Book.find(id)
  Book.book_list.remove(found_book)
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True, port=3000)