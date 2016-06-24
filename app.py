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


# create 'app' module by passing __name__ to Flask class
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/sqlalchemy_app'
db = SQLAlchemy(app)


class Book(db.Model):
  # Creates table name is PostgreSQL DB
  __tablename__ = 'books'

  # Define columns in table
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text())
  author = db.Column(db.Text())

  # NON-DB CODE
  # # Class property: accessible via Book.id or Book.book_list
  # id = 1
  # book_list = []

  # Every book should have title,author,id
  def __init__(self,title,author):
    self.title = title
    self.author = author

    # NON-DB CODE
    # self.id = Book.id
    # # update 'book_list' class property
    # Book.book_list.append(self)
    # # increment id
    # Book.id += 1

  @classmethod
  # With 'classmethod' decorator, first parameter is always the class in which function resides
  # It is implicitly passed as a parameter, so only additional params ('id') need to be
  # explicitly passed
  def find(cls, id):
    return [book for book in cls.book_list if book.id == id][0]

  def __repr__(self):
    return 'title {} - author {}'.format(self.title,self.author)

db.drop_all() # drop tables

db.create_all() # create tables

# See data
cats_cradle = Book('cats cradle', 'kurt') # make a new instance/row
harry_potter = Book('harry potter', 'jk') # make a new instance/row
db.session.add(cats_cradle)
db.session.add(harry_potter)
# or db.session.add_all([cats_cradle, harry_potter])
db.session.commit() # save to the DB
 

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
  books = Book.query.all()
  return render_template('index.html', books=books)

# NEW
@app.route('/books/new')
def new():
  return render_template('new.html')

# SHOW
@app.route('/books/<int:id>')
def show(id):
  return render_template('show.html', book=Book.query.get(id))

# EDIT
@app.route('/books/<int:id>/edit')
def edit(id):
  return render_template('edit.html', book=Book.query.get(id))

# CREATE
@app.route('/books', methods = ['POST'])
def create():
  new_book = Book(request.form['title'], request.form['author'])
  db.session.add(new_book)
  db.session.commit()
  return redirect(url_for('index'))

# UPDATE
@app.route('/books/<int:id>', methods = ['PATCH'])
def update(id):
  found_book = Book.query.get(id)
  found_book.title = request.form['title']
  found_book.author = request.form['author']
  db.session.add(found_book)
  db.session.commit()
  return redirect(url_for('index'))

# DELETE
@app.route('/books/<int:id>', methods = ['DELETE'])
def destroy(id):
  found_book = Book.query.get(id)
  db.session.delete(found_book)
  db.session.commit()
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True, port=3000)