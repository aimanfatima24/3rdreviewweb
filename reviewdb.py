import sqlite3 as db
from flask import session

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
    user_id= session.get("user_id")
    cursor=conn.cursor()
    print(movie, review, user_id, title, rating)
    #add into table movie_review the following parameters. 
    cursor.execute('INSERT INTO movie_review (movie, review, user_id, title, rating) VALUES(?, ?, ?, ?, ?)',
                       (movie, review, user_id, title, rating))
    #commit to database and close connection 
    conn.commit()
    conn.close()
    print("completed")
    
