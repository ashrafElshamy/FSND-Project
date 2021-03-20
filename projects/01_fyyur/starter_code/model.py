
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String),nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    shows = db.relationship("Shows",backref="venues", cascade="all, delete")
    def upcoming_shows(self):
          upcoming = []
          for show in self.shows:
                if(show.start_time>datetime.now()):
                      upcoming.append(show)
          return(upcoming)
    pass



class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String),nullable=False)
    image_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    facebook_link = db.Column(db.String(300))
    shows = db.relationship("Shows",backref="artists" ,cascade="all, delete")
    def upcoming_shows(self):
          upcoming = []
          for show in self.shows:
                if(show.start_time>datetime.now()):
                      upcoming.append(show)
          return(upcoming)
    pass

    # TODO: implement any missing fields, as a database migration using Flask-Migrate



class Shows(db.Model):
     __tablename__ = 'Shows'
     id = db.Column(db.Integer,primary_key=True)
     description  = db.Column(db.String,nullable=True)
     start_time = db.Column(db.DateTime, default = datetime.utcnow)
     artist_id = db.Column(db.Integer,db.ForeignKey(Artist.id)) 
     venue_id = db.Column(db.Integer,db.ForeignKey(Venue.id))
     pass

