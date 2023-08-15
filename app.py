import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from jinja2 import TemplateNotFound
from datamanager.sql_data_manager import SQLiteDataManager
from config import config
from model_manager.movie_models import *

# Initialize flask app and set some parameters value
app = Flask(__name__, instance_relative_config=False)

# initialize the app with the extension and configuration file
app.config.from_object(config)
db.init_app(app)


# create an object of the JSONDataManager class
def object_create():
    try:
        return SQLiteDataManager()
    except FileNotFoundError:
        return render_template('404.html')


# assigns the object to a variable
data_manager = object_create()

# creates all database tables and also records for Genres table
with app.app_context():
    db.create_all()
    # data_manager.create_genre_record()


@app.route('/')
def index():
    """
        Gets triggered when client sends a get request to this route.
        It renders the index.html webpage
    :return:
    """
    try:
        return render_template('index.html')
    except TemplateNotFound:
        return "Template not found", 404


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
        Gets triggered when the client sends either a get request to this route.
        Parses response data and renders the appropriate html document based on app state and condition statements
    :return:
    """
    try:
        # gets the form data from POST url
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            gender = request.form["gender"]

            # calls the add_user method which performs the add operation on the users table
            data_manager.add_user(username, email, password, gender)

            # sends data of this session to the redirected url
            flash(f"The user -- {username} -- has been added successfully.", "success")
            return redirect(url_for("users"))
        else:
            return render_template('add_user.html')
    except(AttributeError, ValueError, TypeError, FileNotFoundError, KeyError, TemplateNotFound,
           sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_user_movie(user_id):
    """
        Gets triggered when the client sends either a get request to this route.
        Parses response data and renders the appropriate html document based on app state and other condition statements
    :param user_id:
    :return:
    """
    try:
        # gets the form data from POST url
        if request.method == "POST":
            title = request.form["title"].strip()
            rating = request.form["rating"]
            director = request.form["director"]
            year = request.form["year"]
            genre_id = int(request.form["genre_id"])

            # calls the add_movie method which performs the add operation on the movies and user_movies tables
            message = data_manager.add_movie(title, rating, director, year, genre_id, user_id)

            # sends data of this session to the redirected url
            flash(f"{message}", "success")
            return redirect(url_for("user_movies", user_id=user_id, ))
        else:
            # checks the state of GET request to determine the template to render and the data to send
            searched_movie = request.args.get("searched_movie")
            if searched_movie is None:
                state = 'get'
                return render_template('add_user_movie.html', state=state, user_id=user_id)
            else:
                title, rating, director, year = data_manager.get_movie_info_api(searched_movie)

                if title is None:
                    flash(f"There are no movies matching your searched movie -- {searched_movie}", "success")
                    return redirect(url_for("user_movies", user_id=user_id))
                else:
                    return render_template('add_user_movie.html', title=title, year=year, rating=rating,
                                           director=director, user_id=user_id)
    except(AttributeError, ValueError, TypeError, FileNotFoundError, KeyError, TemplateNotFound,
           sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
        Gets triggered when the client sends a get request to the route.
        It takes a user_id parameter obtained from the request and renders the user.html webpage which
        display the movies of a particular user
    :param user_id:
    :return:
    """
    try:
        # Handles the flash message sent from other sessions
        flash_message = None
        if len(get_flashed_messages()) > 0:
            flash_message = get_flashed_messages()[0]

        # gets all the records in reviews table
        reviews_data = data_manager.get_all_reviews_data()
        user_movies_list = data_manager.get_user_movies(user_id)
        name = data_manager.get_user_name(user_id)
        genres_details = data_manager.get_genre_details()
        return render_template('user_movies.html', user_movies=user_movies_list, user_id=user_id, name=name,
                               flash_message=flash_message, reviews_data=reviews_data, genres_details=genres_details)
    except (AttributeError, ValueError, TypeError, FileNotFoundError, KeyError, sqlalchemy.exc.NoResultFound,
            sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users/<int:user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    """
        Gets triggered when the client sends either a get or post request to this route.
        Parses response data and renders the appropriate html document based on app state and other condition statements
    :param user_id:
    :param movie_id:
    :return:
    """
    try:
        if request.method == "POST":
            title = request.form["title"].strip()
            director = request.form["director"]
            year = request.form["year"]
            rating = float(request.form["rating"])
            genre_id = int(request.form["genre_id"])

            # catches error raised when a movie with no review is updated, this set the description value to None \
            # and it is used to determine the state of review description field to be visible or not
            try:
                description = request.form["description"]
            except KeyError:
                description = None

            message = data_manager.update_user_movie(user_id, movie_id, genre_id, director, year, description, rating)

            flash(message, "success")
            return redirect(url_for("user_movies", user_id=user_id, title=title))
        else:
            movie_director, movie_year, movie_title = data_manager.get_usermovie_director_year(user_id, movie_id)
            review_description = data_manager.get_userreview_description(user_id, movie_id)
            return render_template('update_user_movie.html', director=movie_director, year=movie_year,
                                   description=review_description, title=movie_title,
                                   user_id=user_id, movie_id=movie_id)
    except (AttributeError, ValueError, TypeError, FileNotFoundError, KeyError,sqlalchemy.exc.NoResultFound,
            sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_user_movie(user_id, movie_id):
    """
        Gets triggered when the client sends a get request to the route
        Parses response data and performs the appropriate operations based on app state and other condition statements
    :param user_id:
    :param movie_id:
    :return:
    """
    try:
        message = data_manager.delete_user_movie(user_id, movie_id)

        flash(message, "success")
        return redirect(url_for("user_movies", user_id=user_id))
    except (AttributeError, ValueError, TypeError, FileNotFoundError, KeyError,sqlalchemy.exc.NoResultFound,
            sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users/<int:user_id>/delete_review/<int:movie_id>')
def delete_user_review(user_id, movie_id):
    """
        Gets triggered when the client sends a get request to the route
        Parses response data and performs the appropriate operations based on app state and other condition statements
    :param user_id:
    :param movie_id:
    :return:
    """
    try:
        message = data_manager.delete_user_review(user_id, movie_id)

        flash(message, "success")
        return redirect(url_for("user_movies", user_id=user_id))
    except (AttributeError, ValueError, TypeError, FileNotFoundError, KeyError,sqlalchemy.exc.NoResultFound,
            sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/users')
def users():
    """
        Gets triggered when the client sends a get request to the route
        It renders users.html webpage which displays users' names
    :return:
    """
    try:
        flash_message = None
        if len(get_flashed_messages()) > 0:
            flash_message = get_flashed_messages()[0]

        users = data_manager.get_all_users()
        return render_template('users.html', users=users, flash_message=flash_message)
    except (AttributeError, ValueError, TypeError, FileNotFoundError, KeyError, sqlalchemy.exc.NoResultFound,
            sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.route('/reviews/<int:user_id>/review_movie/<int:movie_id>', methods=['GET', 'POST'])
def add_user_review(movie_id, user_id):
    """
        Gets triggered when the client sends a get request to the route
        Parses response data and performs the appropriate operations based on app state and other condition statements
    :param movie_id:
    :param user_id:
    :return:
    """
    try:
        if request.method == "POST":
            description = request.form["description"]
            rating = float(request.form["rating"])

            data_manager.add_user_review(movie_id, user_id, description, rating)

            flash(f"Review successfully added to the movie", "success")
            return redirect(url_for("user_movies", user_id=user_id))
    except(AttributeError, ValueError, TypeError, FileNotFoundError, KeyError, TemplateNotFound,
           sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError):
        return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5003)
