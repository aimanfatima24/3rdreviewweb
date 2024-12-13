from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, add_user, verify_password
from reviewdb import init_db, add_review
import sqlite3 as db

app = Flask(__name__)
app.secret_key= 'hessjee'

init_db()

@app.route("/")
def home():
    movies = [
        {"title": "Moana", "image": "static/images/moana2.jpg"}
    ]

    print("Session Data:", session)
    if 'user_id' in session:
        return render_template("loggedin.html", movies=movies, user_email = session['email'])
    else:
        print("not in sesh")
        return render_template("base_not.html")
    
    

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
                session['user_id']=result[0]
                session['email'] =email
                print ("Login successful")
                return render_template("loggedin.html")
                #flash logged in message
            else:
                return "Incorrect username or password"
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

        result = add_user(name, email, dob, password)
        if result == "email exists":
            return "Email already exists!"
        
        return redirect(url_for('login'))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash("You have been logged out")
    return redirect(url_for('base_not.html'))

@app.route("/addreview", methods=["GET", "POST"])
def add_review_route():
    if request.method == "POST":
        movie= request.form.get("movie")
        review= request.form.get("review")
        user_id = session.get("user_id")

        result = add_review(movie, review, user_id)
    return render_template("review.html")
        #flash a message saying flash(f"Review for {movie} added successfully!")
    

    movie= request.args.get("movie")
    return render_template("review.html", movie=movie)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)