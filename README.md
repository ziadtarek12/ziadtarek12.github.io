# MYmovies
#### Video Demo:  <https://www.youtube.com/watch?v=4LkICvMN3f0&ab_channel=ZiadTarek>
#### Description:
Overview
This Flask web application is a simple movie tracker that allows users to add and remove movies to their personal list and search for movies to add. Users can create an account, log in and log out. The application uses SQLite as its database.

Files
application.py: This file contains the main application code. It sets up the Flask application, the session configuration, and the routes.
helpers.py: This file contains helper functions for the application, including the error function and the login_required decorator.
movies.db: This is the SQLite database file that stores the movies and user data.
Dependencies
This application uses the following Python packages:

Flask: a web microframework for Python
cs50: a library that provides access to a SQLite database
Flask-Session: a Flask extension for server-side sessions
Routes
The application has the following routes:

/: the main page of the application, which displays the user's list of movies.
/add: a page where users can add a movie to their list.
/login: a page where users can log in to their account.
/logout: a page where users can log out of their account.
/register: a page where users can create a new account.
/remove: a page where users can remove a movie from their list.
/search: a page where users can search for movies to add to their list.
Templates
The application uses the following HTML templates:

index.html: the template for the main page of the application.
add.html: the template for the add movie page.
login.html: the template for the login page.
register.html: the template for the register page.
search.html: the template for the search page.
searched.html: the template for the search results page.
error.html: the template for error messages.
Features
The application has the following features:

First you can register for an account that has a name (can't be repeated) a password that will you will be asked to confirm then you can log in to the site. you can do many things inside the site first you can search for movies in our database which consists of the top 1000 movies of all time accoriding to IMDB after searching for the film you can choose to add. Add films will make it appear at your home screen. You can also remove films from your home screen using the remove functonality.
The database used is called movies.db it has three tables one called movies that has all information about movies and each movie has a primary key that is a unique id. users table that has all information about the user and each user also has a primary key a unique id. user_movies this table has only two columns movie_id and user_id and both of them are foreign keys that connects to movies through the movie id and users throught the user id. It is basically a table to connect movies and users tables and save the movies that the user possess.
there are three main functionality:
search that return a route/search if you acceses through get it will show you a page in which you can search a movie and sumbit. once you submit which is via post it will redirect you in another page in the same route inwhich it will show you the result of the qurey on the database using the name you provided.

add: in which you can add your movies to your account. When acceseed via get it will show you a page in which you can put a movie name and add it via  a button. When you sumbit the button it sumbits via post runs a query on the database that inserts the movie(if exists) in user_movies table and then redirects you to the homepage where a query on user_movies is run to get the movies coresspendin to you id then a query on movies table is done through these ids and it shows these movies on the homepaage via html code
credits: some of the functions and code were taken from cs50 finance problem