import os
from urllib.parse import quote_plus

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

db_user = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'gobelin_exam'

db_password_encoded = quote_plus(db_password)

SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_password_encoded}@{db_host}/{db_name}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
