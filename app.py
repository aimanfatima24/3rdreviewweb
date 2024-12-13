from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_user, verify_password
import sqlite3 as db

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    return render_template("base.html")

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
                print ("Login successful")
                return redirect(url_for('home'))
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)