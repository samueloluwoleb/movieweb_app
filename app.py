from flask import Flask, render_template, request
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)


# create an object of the JSONDataManager class
def object_create():
    try:
        return JSONDataManager('storage/movies_database.json')
    except FileNotFoundError:
        return render_template('404.html')


data_manager = object_create()


@app.route('/')
def index():
    """
        Gets triggered when client sends a get request to this route.
        It renders the index.html webpage
    :return:
    """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
        Gets triggered when the client sends a get request to the route
        It renders users.html webpage which displays users' names
    :return:
    """
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except (AttributeError, ValueError, TypeError, FileNotFoundError):
        return render_template('404.html')


@app.route('/users/<user_id>')
def show_user_movies(user_id):
    """
        Gets triggered when the client sends a get request to the route.
        It takes a user_id parameter obtained from the request and renders the user.html webpage which
        display the movies of a particular user

    :param user_id:
    :return:
    """
    try:
        user_movies = data_manager.get_user_movies(user_id)
        name = data_manager.get_user_name(user_id)
        return render_template('user_movies.html', user_movies=user_movies, user_id=user_id, name=name)
    except (AttributeError, ValueError, TypeError):
        return render_template('404.html')


@app.route('/add_user')
def add_user():
    """
        Gets triggered when the client sends either a get request to this route.
        Parses response data and renders the appropriate html document based on app state and condition statements

    :return:
    """
    try:
        user_name = request.args.get('username')
        name = ""
        if user_name is None:
            return render_template('add_user.html', user_name=user_name, name=name)
        else:
            if user_name == '':
                return render_template('add_user.html', user_name=user_name)
            else:
                name, user_id = data_manager.add_user(user_name)
                user_name = name
                return render_template('add_user.html', user_name=user_name, name=name, user_id=user_id)
    except (AttributeError, ValueError, TypeError):
        return render_template('404.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_user_movie(user_id):
    """
        Gets triggered when the client sends either a get or post request to this route.
        Parses response data and renders the appropriate html document based on app state and some condition statements
    :param user_id:
    :return:
    """
    try:
        # Parses POST response data and renders the appropriate html document with the appropriate response data
        if request.method == 'POST':
            user_movies = data_manager.get_user_movies(user_id)
            name = request.form['movie_name']
            year = request.form['movie_year']
            rating = request.form['movie_rating']
            director = request.form['movie_director']

            # check if user entered a movie name
            if name.strip() == '':
                movie_name = 'empty name'
                return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)

            # check if user already has the movie with the name that is inputted
            if user_movies:
                for movie in user_movies:
                    if name.strip() == movie.get('name').strip():
                        movie_name = 'movie_exists'
                        return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)

            data_manager.add_user_movie(name, director, year, rating, user_id)
            movie_name = "movie added"

            return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name, name=name)
        # Parses GET response data and renders the appropriate html document with the appropriate response data
        else:
            user_ids_all = data_manager.user_ids()
            if user_id not in user_ids_all:
                return render_template('404.html')

            movie_name = request.args.get('movie_search')
            if movie_name is None:
                return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)
            if movie_name or movie_name == '':
                name, year, rating, director = data_manager.get_movie_info_api(movie_name, user_id)
                if name == 'no movie found':
                    movie_name = name
                    return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)
                if name == 'no search':
                    movie_name = name
                    return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)
                if name == 'movie exists':
                    movie_name = name
                    return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)
                return render_template('add_user_movie.html', movie_name=movie_name, year=year,
                                       rating=rating, director=director, user_id=user_id, name=name)
    except (AttributeError, ValueError, TypeError):
        return render_template('404.html')


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    """
        Gets triggered when the client sends either a get or post request to this route.
        Parses response data and renders the appropriate html document based on app state and some condition statements
    :param user_id:
    :param movie_id:
    :return:
    """
    try:
        movie_id = int(movie_id)

        # Parses POST response data and renders the appropriate html document with the appropriate response data
        if request.method == 'POST':
            user_movies = data_manager.get_user_movies(user_id)
            name = request.form['movie_name']
            year = request.form['movie_year']
            rating = request.form['movie_rating']
            director = request.form['movie_director']

            # check if user entered a movie name
            if name.strip() == '':
                movie_name = 'empty name'
                return render_template('update_user_movie.html', movie_name=movie_name, user_id=user_id)

            # check if user already has the movie with the name that is inputted

            for movie in user_movies:
                if (name.strip() == movie.get('name').strip()) and (movie.get('id') != movie_id):
                    movie_title = 'movie exists'
                    return render_template('update_user_movie.html', movie_title=movie_title, user_id=user_id)

            data_manager.update_movie(name, director, year, rating, user_id, movie_id)
            return render_template('update_user_movie.html', name=name, user_id=user_id)

        # Parses GET response data and renders the appropriate html document with the appropriate response data
        else:
            movie = data_manager.get_user_movie(user_id, movie_id)
            return render_template('update_user_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)
    except (AttributeError, ValueError, TypeError):
        return render_template('404.html')


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_user_movie(user_id, movie_id):
    """
        Gets triggered when the client sends a get request to the route
        Parses response data and renders the appropriate html document based on app state and some condition statements
    :param user_id:
    :param movie_id:
    :return:
    """
    try:
        movie_id = int(movie_id)
        movie_name = data_manager.get_movie_name(user_id, movie_id)
        data_manager.delete_movie(user_id, movie_id)

        return render_template('delete_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
    except (AttributeError, ValueError, TypeError):
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
    app.run(host="0.0.0.0", port=5000, debug=True)
