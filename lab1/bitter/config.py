import os

from dotenv import load_dotenv


load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_STRING')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FILTER = True
