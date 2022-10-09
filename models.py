from email.policy import default
from enum import unique
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true
from flask_migrate import Migrate
from flask import Flask
from datetime import datetime 


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)
  venue = db.relationship('Venue', back_populates='artists_show', lazy=True)
  artist = db.relationship('Artist', back_populates='venues_show', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.ARRAY(db.String()))
    phone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    image_link = db.Column(db.String(200), nullable=True)
    facebook_link = db.Column(db.String(200), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    artists_show = db.relationship('Show', back_populates='venue')

    def __repr__(self):
       return f'/<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(200))
    facebook_link = db.Column(db.String(200))
    website = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    venues_show = db.relationship('Show', back_populates='artist')

    def __repr__(self):
       return f'/<Artist {self.id} {self.name}>'