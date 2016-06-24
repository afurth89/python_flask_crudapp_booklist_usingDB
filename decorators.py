from functools import wraps

def my_first_decorator(fn):
  # Purpose of 'wraps' is to keep internal properties
  # of function passed to decorator ('say_bye')
  # So use of this decorator returns 'say_bye'
  # (instead of 'inner')
  @wraps(fn)
  def inner():
    print('Hello')
    return fn()
  return inner

@my_first_decorator
# Above decorator is same as 'say_bye = my_first_decorator(say_bye)'
def say_bye():
  print('bye')

# 'say_bye' is FIRST CLASS function 
  # (passed to another function)
say_bye()

current_user = dict(id=2)

def is_authorized(id):
  def wrapper(fn):
    @wraps(fn)
    def inner():
      if (current_user.id != id):
        return redirect(url_for('login'))
      return fn()
    return inner
  return wrapper

@app.route('/users/<int:id>/edit')
@is_authorized(id)
def edit(id):
  return render_template('edit', id=id)


@app.route('/users/<int:id>', method=['PATCH'])
@is_authorized(id)
def update(id):
  # Update code here