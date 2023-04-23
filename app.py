import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error, login_required



# Configure application
app = Flask(__name__)

# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")

# Getting user'name


@app.route("/")
@login_required
def index():

    user_info = db.execute("SELECT * FROM movies WHERE id IN (SELECT movie_id FROM user_movies where user_id = ?)", session["user_id"])
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("index.html", user_info=user_info, user_name=user_name)



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":
        movie = request.form.get("movie").strip()
        if not movie:
            return error("NO movie entered")



        movie_id = db.execute("SELECT id FROM movies WHERE name = ?", movie)
        if movie_id:
            try:
                db.execute("INSERT INTO user_movies VALUES (?, ?)", movie_id[0]["id"], session["user_id"])
            except ValueError:
                return error("Movie already added")
        else:
            return error("no movie with that name")
        return redirect("/")
    else:
        return render_template("add.html", user_name=user_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]


    if request.method == "POST":
        if request.form.get("movie"):
            movies = db.execute("SELECT id, name, RATING,  director, time, year FROM movies WHERE name LIKE ?", "%" + request.form.get("movie").strip() + "%")

        else:
            return error("Please enter movie name")
        if movies:
            clicked = request.form.get("add")
            if clicked:
                db.execute("INSERT INTO user_movies VALUES(?, ?)", clicked, session["user_id"])
            return render_template("searched.html", movies=movies, user_name=user_name)
        else:
            return error("no movies with that name")
    else:
        return render_template("search.html", user_name=user_name)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        user_name = request.form.get("username")
        if not user_name:
            return error("NO name")
        user_password = request.form.get("password")
        if not user_password:
            return error("NO password")

        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return error("Please confirm password")

        if user_password != confirm_password:
            return error("Passwords doesn't match")
        check = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", user_name)
        if check[0]["COUNT(*)"] != 0:
            return error("user name already taken")

        hashed_password = generate_password_hash(user_password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user_name, hashed_password)
        session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", user_name)[0]["id"]
        return redirect("/")
    return render_template("register.html")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]


    movies = db.execute("SELECT name from movies WHERE id IN (SELECT movie_id FROM user_movies WHERE user_id = ?)", session["user_id"])
    if request.method == "POST":
        movie_name = request.form.get("movie").replace("{'name':", "").replace("}", "").replace("'", "").strip()
        if not movie_name:
            return error("NO movie name")

        db.execute("DELETE FROM user_movies WHERE movie_id = (SELECT id FROM movies WHERE name = ?)", movie_name)
        return redirect("/")

    else:
        return render_template("remove.html", movies=movies, user_name=user_name)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":
        user_password = request.form.get("password")
        if not user_password:
            return error("NO password")

        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return error("Please confirm password")

        if user_password != confirm_password:
            return error("Passwords doesn't match")

        hashed_password = generate_password_hash(user_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, session["user_id"])

        return redirect("/")
    else:
        return render_template("change.html", user_name=user_name)