import json
import requests
from datamanager.data_manager_interface import DataManagerInterface

API_KEY_MOVIES = '1081add1'


class JSONDataManager(DataManagerInterface):

    @staticmethod
    def load_data(file_path):
        """
            Locate a JSON database file and loads it into the program
        """
        try:
            with open(file_path, "r") as handle:
                return json.load(handle)
        except (IOError, FileNotFoundError) as e:
            print("An Error Occurred:", str(e))

    def __init__(self, file_path):
        """
            The constructor to initialize the objects of this class, it takes the database file path as argument
            :param file_path:
        """
        self._file_path = file_path

    def get_all_users(self):
        """
            Return a list of all users in the database
        :return:
        """
        try:
            users = self.load_data(self._file_path)
            return users
        except (IOError, FileNotFoundError) as e:
            print("An Error Occurred:", str(e))

    def get_user_movies(self, user_id_param):
        """
            Return a list of all movies for a given user. It takes user id as parameter and returns a list of the
            user's favourite movies
        :param user_id_param:
        :return:
        """
        try:
            users = self.get_all_users()
            return users[0].get(user_id_param).get('movies')
        except (AttributeError, ValueError, TypeError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def add_user(self, name):
        """
            creates new user by taking a username parameter and auto-generating user_id, then add user to database
        :param name:
        :return name:
        """
        try:
            users = self.get_all_users()

            # generates user id, add the user name and user id to the database
            new_id = max(int(user_id) for user_id in users[0]) + 1
            new_id = str(new_id)
            users[0][new_id] = {'name': name}

            json_data = json.dumps(users)

            with open("storage/movies_database.json", "w") as fileobj:
                fileobj.write(json_data)

            return name, new_id
        except (AttributeError, ValueError, TypeError, FileNotFoundError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def get_movie_info_api(self, movie_name_param, user_id_param):
        """
            Searches the web through an api for more details about a searched movie and manipulate the response
            accordingly
        :param movie_name_param:
        :param user_id_param:
        :return:
        """
        try:
            search_title = movie_name_param
            url = f"https://www.omdbapi.com/?apikey={API_KEY_MOVIES}&t={search_title}"
            response = requests.get(url)
            response = response.json()

            # check if user doesn't enter a search word
            if response['Response'] == 'False':
                if response['Error'] == 'Movie not found!':
                    return 'no movie found', '', '', ''
                if response['Error'] == 'Incorrect IMDb ID.':
                    return 'no search', '', '', ''
            else:
                # Get the data from response
                name = response.get('Title')
                director = response.get('Director')
                year = response.get('Year')
                rating = response.get('imdbRating')

                # check if user already has the movie that was searched
                user_movies = self.get_user_movies(user_id_param)
                if user_movies:
                    for movie in user_movies:
                        if name.strip() == movie.get('name').strip():
                            return 'movie exists', '', '', ''

                # return the appropriate movie info
                return name, year, rating, director
        except (AttributeError, ValueError, TypeError, ConnectionError) as e:
            print("An Error Occurred:", str(e))
            return None, None, None, None

    def add_user_movie(self, name_param, director_param, year_param, rating_param, user_id_param):
        """
            Gets some movie info parameters, parse the movie details to create a movie dictionary object and
            add the movie dictionary object to the right user in the database
        :param name_param:
        :param director_param:
        :param year_param:
        :param rating_param:
        :param user_id_param:
        :return:
        """
        try:
            users = self.get_all_users()
            movies = self.get_user_movies(user_id_param)

            # create a movie id based on if user already has some movies added or not
            if not movies:
                movie_id = 1
                movies = []
            else:
                movie_id = int(max(movie.get('id') for movie in movies)) + 1

            # create a movie dictionary object to be added to the user movie and update database file with the object
            movie_info = {
                "id": movie_id,
                "name": name_param,
                "director": director_param,
                "year": year_param,
                "rating": rating_param
            }
            movies.append(movie_info)
            users[0].get(user_id_param)["movies"] = movies

            json_data = json.dumps(users)

            with open("storage/movies_database.json", "w") as fileobj:
                fileobj.write(json_data)
        except (AttributeError, ValueError, TypeError, IOError, FileNotFoundError) as e:
            print("An Error Occurred:", str(e))
            return None

    def get_user_movie(self, user_id_param, movie_id_param):
        """
            Returns the appropriate movie that belong to a user with the given user id and movie id
        :param user_id_param:
        :param movie_id_param:
        :return movie:
        """
        try:
            user_movies = self.get_user_movies(user_id_param)
            for movie in user_movies:
                if movie.get('id') == movie_id_param:
                    return movie
        except (AttributeError, ValueError, TypeError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def get_movie_name(self, user_id_param, movie_id_param):
        """
            Returns the appropriate movie name that belong to a user with the given user id and movie id
        :param user_id_param:
        :param movie_id_param:
        :return:
        """
        try:
            user_movies = self.get_user_movies(user_id_param)
            for movie in user_movies:
                if movie.get('id') == movie_id_param:
                    return movie.get('name')
        except (AttributeError, ValueError, TypeError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def update_movie(self, name_param, director_param, year_param, rating_param, user_id_param, movie_id_param):
        """
            Gets some movie info as parameters and update the appropriate user and user movies with the new movies info
            given the user id and movie id provided
        :param name_param:
        :param director_param:
        :param year_param:
        :param rating_param:
        :param user_id_param:
        :param movie_id_param:
        :return:
        """
        try:
            users = self.get_all_users()
            movies = self.get_user_movies(user_id_param)

            movie_info = {"id": movie_id_param, "name": name_param, "director": director_param,
                          "year": year_param, "rating": rating_param}
            for count, movie in enumerate(movies):
                if movie.get('id') == movie_id_param:
                    users[0].get(user_id_param).get("movies")[count] = movie_info

            json_data = json.dumps(users)
            with open("storage/movies_database.json", "w") as fileobj:
                fileobj.write(json_data)
        except (AttributeError, ValueError, TypeError, FileNotFoundError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def delete_movie(self, user_id_param, movie_id_param):
        """
            Gets a user id and movie id as parameter and deletes the user movie that matches the appropriate user and
            movie id.
        :param user_id_param:
        :param movie_id_param:
        :return:
        """
        try:
            users = self.get_all_users()
            movies = self.get_user_movies(user_id_param)

            for count, movie in enumerate(movies):
                if movie_id_param == movie.get('id'):
                    del users[0].get(user_id_param).get('movies')[count]

                    json_data = json.dumps(users)
                    with open("storage/movies_database.json", "w") as fileobj:
                        fileobj.write(json_data)
        except (AttributeError, ValueError, TypeError, FileNotFoundError, ConnectionError) as e:
            print("An Error Occurred:", str(e))

    def get_user_name(self, user_id_param):
        """
            Returns the appropriate user name that belong to a user with the given user id parameter
        :param user_id_param:
        :return:
        """
        try:
            users = self.get_all_users()
            return users[0].get(user_id_param).get('name')
        except (AttributeError, ValueError, TypeError, FileNotFoundError, ConnectionError) as e:
            print("An Error Occurred:", str(e))
