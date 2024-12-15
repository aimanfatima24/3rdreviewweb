from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, add_user, verify_password
from reviewdb import init_database, add_review
import sqlite3 as db

app = Flask(__name__)
app.secret_key= 'hessjee'

init_db()
init_database()

@app.before_request
def before_request():
    # Check if the session has been initialized
    if 'initialized' not in session:
        session.clear()  # Clear the session
        session['initialized'] = True  # Set the flag to indicate session has been initialized


@app.route("/")
def home():
    movies = [
        {"title": "Moana", "image": "static/images/moana2.jpg"}
    ]

    print("Session Data:", session)
    return render_template("base_not.html")
    

@app.route("/homepage")
def homepage():
    if 'user_id':
        return render_template('base.html')
    

@app.route("/login",  methods=['GET', 'POST'])
def login():
    data= request.form
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']

        conn = db.connect('registration.db')
        cursor= conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email= ?", (email,))
        result= cursor.fetchone()
        conn.close()


        if result:
            stored_password = result[0]
            if verify_password(stored_password, password):
                session['user_id']= result[0]
                session['email'] =email
                print ("Login successful")
                return render_template("loggedin.html")
                #flash logged in message
            else:
                flash("Incorrect username or password", category="error")
                return redirect(url_for('login'))
        else:
            return "No user found"
        
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        user_id = session.get("user_id")

        if len(password) <5:
            flash("Password too short", category="error")
        elif len(name) <2:
            flash("Please enter a valid name", category="error")
        
        conn = db.connect('registration.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user= cursor.fetchone()
        conn.close()

        if existing_user:
            flash('email already exists!', category="error")
            return redirect(url_for('signup'))

        result = add_user(user_id, name, email, dob, password)
        if result == "email exists":
            return redirect(url_for('signup'))
                    
        return redirect(url_for('login'))

    return render_template("signup.html")


@app.route("/addreview", methods=["GET", "POST"])

def add_review_route():
    if request.method == "POST":
        movie= request.form.get("movie")
        review= request.form.get("review")
        title= request.form.get("title")
        rating= request.form.get("rating")
        user_id = session.get("user_id")
        print(f'User id={user_id}')

        result = add_review(movie, review, user_id, title, rating)
    return render_template("review.html")
        #flash a message saying flash(f"Review for {movie} added successfully!")
    

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    print("Session after logout:", session)
    #flash("You have been logged out")
    return render_template('base.html')


def get_user_by_id(user_id):
    conn=db.connect('registration.db')
    cursor=conn.cursor()
    #user_id='scrypt:32768:8:1$hPQbrKiHeq0R6WkX$dcd41ad7557192faaeaf1b542f184325155df463df9fe7c7d364f28a7e98d6f2078d01b08de2b8dfcb584d6d3b8a2b001395b63cba4e56cb88c62f27376d287b'
    #user_id = session.get('user_id')
    print(f'userid={user_id}')
    print(f'Executing query: SELECT name FROM users WHERE password="{user_id}"')

    cursor.execute ("SELECT name FROM users WHERE password=?", (user_id,))
    result=cursor.fetchone()
    print(f'name is {result[0]}')
    conn.close()
    
    return result[0]

@app.route("/view")
def view():
    user_id = session.get('user_id')
    print(f'user id is:{user_id}')
    conn=db.connect('review.db')
    cursor=conn.cursor()

    cursor.execute("SELECT movie, title, created_at, review, rating FROM movie_review WHERE user_id=?", (user_id,))
    reviews = cursor.fetchall()
    conn.close()

    if user_id:
        user_name = get_user_by_id(user_id)
        print(f'user name is {user_name}')
        return render_template("view.html", name=user_name, reviews=reviews)
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    
@app.route("/viewall")
def viewall():
    user_id = session.get('user_id')
    conn_reviews = db.connect('review.db')
    cursor_reviews = conn_reviews.cursor()

    # Attach the second database (users)
    conn_reviews.execute("ATTACH DATABASE 'registration.db' AS users_db")
    
    # Fetch reviews with the user's name using a JOIN
    cursor_reviews.execute("""
        SELECT 
            movie_review.movie, 
            movie_review.title, 
            movie_review.created_at, 
            movie_review.review, 
            movie_review.rating, 
            users_db.users.name
        FROM movie_review
        JOIN users_db.users ON movie_review.user_id = users_db.users.user_id
    """)
    reviews = cursor_reviews.fetchall()
    
    conn_reviews.close()
    
    if user_id:
        return render_template("view.html", reviews=reviews)
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)