import sqlite3 as db

DATABASE= 'review.db'

def init_db():
    conn= db.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   user_id INTEGER NOT NULL,
                   movie TEXT NOT NULL,
                   review TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   );

''')
    conn.commit()
    conn.close()


def add_review(movie, review, user_id):
    """
    Adds a new review to the database.
    
    """
    conn=db.connect(DATABASE)
    cursor=conn.cursor()
    try:
        print(movie, review, user_id)
        cursor.execute('INSERT INTO reviews (movie, review, user_id) VALUES(?, ?, ?)',
                       (movie, review, user_id))
    finally:
        conn.close()
