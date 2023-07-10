from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import json

app = Flask(__name__)

# create an object of the JSONDataManager class
data_manager = JSONDataManager('storage/movies_database.json')


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
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def show_user_movies(user_id):
    """
        Gets triggered when the client sends a get request to the route.
        It takes a user_id parameter obtained from the request and renders the user.html webpage which
        display the movies of a particular user

    :param user_id:
    :return:
    """
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_movies=user_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
        Gets triggered when the client sends either a get or post request to this route.

    :return:
    """
    if request.method == 'POST':
        name = request.form['username']
        data_manager.add_user(name)
        return redirect(url_for('list_users'))
    else:
        return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_user_movie(user_id):
    if request.method == 'POST':
        name = request.form['movie_name']
        year = request.form['movie_year']
        rating = request.form['movie_rating']
        director = request.form['movie_director']

        data_manager.add_user_movie(name, director, year, rating, user_id)

        return redirect(url_for('show_user_movies', user_id=user_id))
    else:
        movie_name = request.args.get('movie_search')
        if movie_name is None:
            return render_template('add_user_movie.html', user_id=user_id, movie_name=movie_name)
        if movie_name or movie_name == '':
            name, year, rating, director = data_manager.get_movie_info_api(movie_name, user_id)
            print(name, year, rating, director)
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


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    movie_id = int(movie_id)
    if request.method == 'POST':
        name = request.form['movie_name']
        year = request.form['movie_year']
        rating = request.form['movie_rating']
        director = request.form['movie_director']

        data_manager.update_movie(name, director, year, rating, user_id, movie_id)

        return redirect(url_for('show_user_movies', user_id=user_id))
    else:
        id_movie = request.args.get('update_movie')
        if movie_name is None:
            return render_template('update_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
        if movie_name or movie_name == '':
            name, year, rating, director = data_manager.get_movie_info_update(movie_name, user_id, movie_id)

            if name == 'no match':
                movie_name = name
                return render_template('update_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
            if name == 'no search':
                movie_name = name
                return render_template('update_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
            return render_template('update_user_movie.html', name=name, movie_id=movie_id,
                                   year=year, rating=rating, director=director, user_id=user_id)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_user_movie(user_id, movie_id):
    movie_id = int(movie_id)
    movie_name = request.args.get('delete_movie')
    if movie_name is None:
        return render_template('delete_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
    if movie_name or movie_name == '':
        name = data_manager.delete_movie(movie_name, user_id, movie_id)
        if name == "no match":
            movie_name = name
            return render_template('delete_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
        if name == "no search":
            movie_name = name
            return render_template('delete_user_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie_name)
        if name == "deleted":
            return redirect(url_for('show_user_movies', user_id=user_id))


if __name__ == '__main__':
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
