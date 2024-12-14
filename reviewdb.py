import sqlite3 as db

DATABASE= 'review.db'

def init_database():
    conn= db.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_review(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   user_id TEXT,
                   movie TEXT,
                   review TEXT,
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
    print(DATABASE)
    cursor=conn.cursor()
    print(movie, review, user_id)
    cursor.execute('INSERT INTO movie_review (movie, review, user_id) VALUES(?, ?, ?)',
                       (movie, review, user_id))
    conn.commit()
    conn.close()
    print("completed")


    #cursor.execute('INSERT INTO reviews (movie, review, user_id) VALUES(?, ?, ?)',
                       #(movie, review, user_id))
    
