from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  address = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
  seeking_talent = db.Column(db.Boolean(), default=True)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='venue', cascade="all, delete-orphan")

class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
  seeking_venue = db.Column(db.Boolean(), default=True)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='artist', cascade="all, delete-orphan")

class Show(db.Model):
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  start_time = db.Column(db.DateTime(), primary_key=True)