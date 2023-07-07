from flask import Flask, render_template, request
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)

# create an object of the JSONDataManager class
data_manager = JSONDataManager('movies_database.json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movie(user_id):
    user_name = request.args['name']
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movie.html', user_movies=user_movies, user_name=user_name)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['username']

        users = data_manager.get_all_users()

        new_id = int(max(user_ids for user_ids in users[0])) + 1
        new_id = str(new_id)
        result = {}
        for item in users:
            result.update(item)
        print(result)

    else:
        return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie')
def add_user_movie():
    return render_template('add_user_movie.html')


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_user_movie():
    return render_template(update_user_movie.html)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_user_movie():
    return render_template(delete_user_movie.html)


if __name__ == '__main__':
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
