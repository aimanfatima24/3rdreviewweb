import sqlite3 as db

DATABASE= 'review.db'

def init_database():
    conn= db.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_review(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   user_id TEXT,
                   review title TEXT,
                   rating INTEGER,
                   movie TEXT,
                   review TEXT,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   );

''')
    conn.commit()
    conn.close()


def add_review(movie, review, user_id, title, rating):
    """
    Adds a new review to the database.
    
    """
    conn=db.connect(DATABASE)
    print(DATABASE)
    cursor=conn.cursor()
    print(movie, review, user_id, title, rating)
    cursor.execute('INSERT INTO movie_review (movie, review, user_id, title, rating) VALUES(?, ?, ?, ?, ?)',
                       (movie, review, user_id, title, rating))
    conn.commit()
    conn.close()
    print("completed")
    
