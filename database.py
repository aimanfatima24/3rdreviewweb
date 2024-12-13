import sqlite3 as db
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'registration.db'

def init_db():
  conn = db.connect(DATABASE)
  cursor=conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 dob DATE NOT NULL,
                 password TEXT NOT NULL             
                                  
                 )
''')
  conn.commit()
  conn.close()
  print('database initialised!')

def add_user(name, email, dob, password):
  """
  Adds a new user to the database. 
  Returns 'email_exists' if the email is already in use.
  """
  hashed_password = generate_password_hash(password)

  conn= db.connect(DATABASE)
  cursor= conn.cursor()
  try:
        cursor.execute('INSERT INTO users (name, email, dob, password) VALUES(?, ?, ?, ?)',
                       (name, email, dob, hashed_password))
        conn.commit()
        print('user added success')
  except db.IntegrityError:  # Changed 'sqlite3' to 'db'
        conn.close()
        return "email_exists"
  conn.close()
  return "Account created!"

def verify_password(stored_password, provided_password):
    """
    Verify a provided password against the stored hash password.
    Returns True if the password matches, False otherwise.
    """
    return check_password_hash(stored_password, provided_password)
        