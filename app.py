from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, add_user, verify_password
from reviewdb import init_database, add_review
import sqlite3 as db

#initialise the flask app
app = Flask(__name__)
app.secret_key= 'hessjee' #creates a secret key essential for session management

#this initialises the database for both registration and reviews.
init_db()
init_database()

#before the app starts, do the following
@app.before_request
def before_request():
    # Check if the session has been initialized
    if 'initialized' not in session:
        session.clear()  # Clear the session
        session['initialized'] = True  #indicate session has been initialized


#creating the home route which is the default when app opens initially.
@app.route("/")
def home():
    #example movie data for the homepage.
    movies = [
        {"title": "Moana", "image": "static/images/moana2.jpg"}
    ]

    #debugging statement to see if the session works
    print("Session Data:", session)
    return render_template("base_not.html") #render the template for when users are not logged in
    

#this creates a route for home when users are logged in 
@app.route("/homepage")
def homepage():
    if 'user_id': #if users are logged in then render the main homepage
        return render_template('base.html')
    

#this is the route when users click on the login button 
@app.route("/login",  methods=['GET', 'POST']) #data is retrieved and posted to the form
def login():
    #get the data from the form 
    data= request.form
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']

        #connect to the datbase
        conn = db.connect('registration.db')
        cursor= conn.cursor()
        #select the password from the table where email provided matches email from the database
        #as email is unique, this will retrieve the correct password associated with the user
        cursor.execute("SELECT password FROM users WHERE email= ?", (email,))
        #retrieve one value only and store in result variable
        result= cursor.fetchone()
        conn.close()

        #if the result, i.e. password from the database matches the password from the form:
        #render the template for when user is logged in
        if result:
            stored_password = result[0]
            if verify_password(stored_password, password):
                session['user_id']= result[0]
                session['email'] =email
                print ("Login successful")
                return render_template("loggedin.html")
                #flash logged in message
            #otherwise, the user has entered something wrong, falsh a message.
            else:
                flash("Incorrect username or password", category="error")
                return redirect(url_for('login'))
        else:
            return "No user found"
        
    return render_template("login.html")


#this is the route for user signup 
@app.route("/signup", methods=['GET', 'POST'])
#get all data from the html form
def signup():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        #get the user id of the session
        user_id = session.get("user_id")

        #validate some fields of the form
        #if password too short, flash a message
        #if name is not valid, then flash a error message
        if len(password) <5:
            flash("Password too short", category="error")
        elif len(name) <2:
            flash("Please enter a valid name", category="error")


        #connect the registration database
        conn = db.connect('registration.db')
        cursor = conn.cursor()
        #get all data from users table where email matches provided email
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user= cursor.fetchone()
        conn.close()


        #if the email exists in the database, error
        if existing_user:
            flash('email already exists!', category="error")
            return redirect(url_for('signup'))

        #call the add_user function so everything is added to the database
        result = add_user(user_id, name, email, dob, password)
        if result == "email exists":
            return redirect(url_for('signup'))
        #if the email already exists, send them back to the signup page.
                    
        return redirect(url_for('login'))

    return render_template("signup.html")


#create route for users to add a review
@app.route("/addreview", methods=["GET", "POST"])

#function to add a review
#gets all data from the form 
#retrieves the user_id from the session
def add_review_route():
    if request.method == "POST":
        movie= request.form.get("movie")
        review= request.form.get("review")
        title= request.form.get("title")
        rating= request.form.get("rating")
        user_id = session.get("user_id")
        print(f'User id={user_id}')

        #adds all the review fields to the database.
        result = add_review(movie, review, user_id, title, rating)
    return render_template("review.html")
        #flash a message saying flash(f"Review for {movie} added successfully!")
    

#logs users out route 
@app.route("/logout")
def logout():
    #clears user_id from the session to become 'None'
    #clears email from the session to become 'None'
    session.pop('user_id', None)
    session.pop('email', None)
    #debugging statement to see if function works well
    print("Session after logout:", session)
    #flash("You have been logged out")
    #after they log out, rendertemplate for logout.
    return render_template('base.html')



#function to get the user name from their user_id
def get_user_by_id(user_id):
    #connect to registration database 
    conn=db.connect('registration.db')
    cursor=conn.cursor()
    #user_id='scrypt:32768:8:1$hPQbrKiHeq0R6WkX$dcd41ad7557192faaeaf1b542f184325155df463df9fe7c7d364f28a7e98d6f2078d01b08de2b8dfcb584d6d3b8a2b001395b63cba4e56cb88c62f27376d287b'
    #user_id = session.get('user_id')
    #debug to check user_id
    print(f'userid={user_id}')
    print(f'Executing query: SELECT name FROM users WHERE password="{user_id}"')

    # from the users table select name where the hashed password = to user id
    #reason for this is user_id was accidentally assigned to hashed password value earlier on in the code
    #changing that would mess up previous functions.
    cursor.execute ("SELECT name FROM users WHERE password=?", (user_id,))
    #retrieve only one value
    result=cursor.fetchone()
    print(result)
    conn.close()
    
    #if user name exists, then print it 
    if result:
        return result[0]
    else:
        return 'hey'



#app route to view user's own comments
@app.route("/view")
def view():
    #get the user_id from the session
    user_id = session.get('user_id')
    print(f'user id is:{user_id}')
    #connect to review_db
    conn=db.connect('review.db')
    cursor=conn.cursor()

    #select all the fields from the movie_review table
    cursor.execute("SELECT movie, title, created_at, review, rating FROM movie_review WHERE user_id=?", (user_id,))
    reviews = cursor.fetchall()
    conn.close()

    #if user_id has some value, then call the get_user_by_id function to get their username
    if user_id:
        user_name = get_user_by_id(user_id)
        print(f'user name is {user_name}')
        #render the view comments html and pass the name as the username and reviews as reviews
        #the form can them use these parameters to display the values
        return render_template("view.html", name=user_name, reviews=reviews)
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    

#route to view all comments from all users
@app.route("/viewall")
def viewall():
    user_id = session.get('user_id')
    conn_reviews = db.connect('review.db')
    cursor_reviews = conn_reviews.cursor()

    # attach the second database (users)
    conn_reviews.execute("ATTACH DATABASE 'registration.db' AS users_db")
    
    # fetch reviews with the user's name using a JOIN
    # allows us to get data from both databases in one query. 
    cursor_reviews.execute("""
        SELECT 
            movie_review.movie, 
            movie_review.title, 
            movie_review.created_at, 
            movie_review.review, 
            movie_review.rating, 
            users.name
        FROM movie_review
        JOIN users_db.users ON movie_review.user_id = users_db.users.user_id
        ORDER BY movie_review.created_at DESC
    """)
    #fetch all the values defined in the query above
    reviews = cursor_reviews.fetchall()
    print(f'Reviews fetched{reviews}')
    
    conn_reviews.close()
    
    if user_id:
        return render_template("viewall.html", reviews=reviews)
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))



if __name__ == '__main__':
    init_db() #initialise the database
    app.run(debug=True, port=5000) #debug and run on port 5000 which is a development server.