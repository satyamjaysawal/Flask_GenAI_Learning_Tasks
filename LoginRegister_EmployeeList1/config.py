import os

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:satyam#567@localhost/dblr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
