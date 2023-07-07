import json
from data_manager_interface import DataManagerInterface


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
        movies_data_list = []
        movies_data = self.load_data(self._file_path)
        movies_data_list.append(movies_data)
        return movies_data_list

    def get_user_movies(self, user_id_param):
        """
            Return a list of all movies for a given user which has the provided id
        :param user_id_param:
        :return:
        """
        movies_data = self.get_all_users()
        return movies_data[0].get(user_id_param).get('movies')

    @staticmethod
    def find_user_by_id(users_param, user_id_param):
        user_id_to_string = str(user_id_param)
        return users_param[0].get(user_id_to_string)


# try:
#     movie1 = JSONDataManager('movies_database.json')
# except (TypeError, json.decoder.JSONDecodeError, FileNotFoundError):
#     print("Check the file path, make sure it is the right json database file")
# print(movie1.get_all_users())
# print(movie1.get_user_movies(1))
# print(movie1.get_user_movies(2))
# print(movie1.find_user_by_id(movie1.get_all_users(), 3))
