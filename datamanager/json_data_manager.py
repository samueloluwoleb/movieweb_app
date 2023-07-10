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
        with open(file_path, "r") as handle:
            return json.load(handle)

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
        users = self.load_data(self._file_path)
        return users

    def get_user_movies(self, user_id_param):
        """
            Return a list of all movies for a given user. It takes user id as parameter and returns a list of the
            user's favourite movies
        :param user_id_param:
        :return:
        """
        users = self.get_all_users()
        return users[0].get(user_id_param).get('movies')

    def add_user(self, name):
        users = self.get_all_users()

        # creates new user_id, create a new user using their name and user_id and add it to the user database
        new_id = int(max(user_ids for user_ids in users[0])) + 1
        new_id = str(new_id)
        users[0][new_id] = {'name': name}

        json_data = json.dumps(users)

        with open("storage/movies_database.json", "w") as fileobj:
            fileobj.write(json_data)

    def get_movie_info_api(self, movie_name_param, user_id_param):
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

                print(name, director, year, rating)

                # check if user already has the movie that was searched
                user_movies = self.get_user_movies(user_id_param)

                if user_movies:
                    for movie in user_movies:
                        if name.strip() == movie.get('name').strip():
                            return 'movie exists', '', '', ''

                return name, year, rating, director
        except Exception:
            return None, None, None, None

    def add_user_movie(self, name_param, director_param, year_param, rating_param, user_id_param):
        try:
            users = self.get_all_users()
            movies = self.get_user_movies(user_id_param)

            # create a movie id based on if user has some movies or not
            if not movies:
                movie_id = 1
                movies = []
            else:
                movie_id = int(max(movie.get('id') for movie in movies)) + 1

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
        except Exception:
            return None

    def get_user_movie(self, user_id_param, movie_id_param):
        user_movies = self.get_user_movies(user_id_param)
        for movie in user_movies:
            if movie.get('id') == movie_id_param:
                return movie

    def get_movie_name(self, user_id_param, movie_id_param):
        user_movies = self.get_user_movies(user_id_param)
        for movie in user_movies:
            if movie.get('id') == movie_id_param:
                return movie.get('name')

    def update_movie(self, name_param, director_param, year_param, rating_param, user_id_param, movie_id_param):

        users = self.get_all_users()
        movies = self.get_user_movies(user_id_param)

        movie_info = {"id": movie_id_param, "name": name_param, "director": director_param, "year": year_param, "rating": rating_param}
        for count, movie in enumerate(movies):
            if movie.get('id') == movie_id_param:
                users[0].get(user_id_param).get("movies")[count] = movie_info

        json_data = json.dumps(users)
        with open("storage/movies_database.json", "w") as fileobj:
            fileobj.write(json_data)

    def delete_movie(self, user_id_param, movie_id_param):

        users = self.get_all_users()
        movies = self.get_user_movies(user_id_param)

        for count, movie in enumerate(movies):
            if movie_id_param == movie.get('id'):
                del users[0].get(user_id_param).get('movies')[count]

                json_data = json.dumps(users)
                with open("storage/movies_database.json", "w") as fileobj:
                    fileobj.write(json_data)


# def find_user_by_id(self, user_id_param):
#     users = self.get_all_users()
#     return users[0].get(user_id_param)
# try:
#     movie1 = JSONDataManager('storage/movies_database.json')
# except (TypeError, json.decoder.JSONDecodeError, FileNotFoundError):
#     print("Check the file path, make sure it is the right json database file")
# print(movie1.get_all_users())
# print(movie1.get_user_movies('1'))
# print(movie1.get_user_movies('2'))
# print(movie1.find_user_by_id(movie1.get_all_users(), '1'))
