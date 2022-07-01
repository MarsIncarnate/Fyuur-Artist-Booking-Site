import os
SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:profaim07112002@localhost:5432/fyuur'

SQLALCHEMY_TRACK_MODIFICATIONS = 'False'