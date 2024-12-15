import sqlite3

# Connect to the review database
conn = sqlite3.connect('review.db')
cursor = conn.cursor()

# Query to find orphaned reviews
cursor.execute("""
    SELECT * 
    FROM movie_review 
    WHERE user_id NOT IN (SELECT user_id FROM users);
""")

# Fetch and print the orphaned reviews
orphaned_reviews = cursor.fetchall()
print("Orphaned Reviews:", orphaned_reviews)

# Close the connection
conn.close()
