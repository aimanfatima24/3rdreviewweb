import sqlite3 as db
from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'registration.db'

def init_db():
  #connect to defined database
  conn = db.connect(DATABASE)
  cursor=conn.cursor()
  #create a table if it doesnt exist called users
  #it shoudl include id, user_id..in the data type mentioned
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id TEXT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 dob DATE NOT NULL,
                 password TEXT NOT NULL             
                                  
                 )
''')
  #commit changes to database so changes are saved 
  conn.commit()
  conn.close()
  print('database initialised!')

#create function to add a user with the parameters given 
def add_user(user_id, name, email, dob, password):
  """
  Adds a new user to the database. 
  Returns 'email_exists' if the email is already in use.
  """
  #use the inbuilt function to generate a hashed password
  hashed_password = generate_password_hash(password)

  conn= db.connect(DATABASE)
  cursor= conn.cursor()

  #seelct everything from users table where email in table mathches email from form
  cursor.execute("SELECT * FROM users WHERE email=?", (email,))
  existing_user= cursor.fetchone()

  if existing_user:
      conn.close()
      flash("email already exists!", category="error")
      return redirect(url_for('signup'))
  else:
    try:
          #insert into the table the parameters given
          cursor.execute('INSERT INTO users (user_id, name, email, dob, password) VALUES(?, ?, ?, ?, ?)',
                        (user_id, name, email, dob, hashed_password))
          conn.commit()
          print('user added success')
    #if there is an error in inserting print error message
    except db.IntegrityError:  # Changed 'sqlite3' to 'db'
          conn.close()
          return "exists"
  conn.close()
  return "Account created!"
#call verification function to compare stroed password with the user's given password. 
def verify_password(stored_password, provided_password):
    """
    Verify a provided password against the stored hash password.
    Returns True if the password matches, False otherwise.
    """
    #check if they match. True or false value is the output.
    return check_password_hash(stored_password, provided_password)
        