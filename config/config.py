import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
RELATIVE_PATH_TO_DATABASE = '../storage/movies.sqlite'
DATABASE_PATH = os.path.join(CURRENT_DIRECTORY, RELATIVE_PATH_TO_DATABASE)
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
SECRET_KEY = '9752-24676'

