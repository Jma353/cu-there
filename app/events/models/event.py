from . import *

class Event(Base):
  __tablename__ = 'events'
  id              = db.Column(db.String, primary_key=True)
  name            = db.Column(db.String)
  category        = db.Column(db.String)
  distance        = db.Column(db.Float)
  attending       = db.Column(db.Integer)
  noreply         = db.Column(db.Integer)
  declined        = db.Column(db.Integer)
  maybe           = db.Column(db.Integer)
  description     = db.Column(db.Text)
  start_time      = db.Column(db.String)
  end_time        = db.Column(db.String)
  profile_picture = db.Column(db.String)
  cover_picture   = db.Column(db.String)
  time_from_now   = db.Column(db.Integer)
  type            = db.Column(db.String)

  # Relationship to venue
  venue_id  = db.Column(db.String, db.ForeignKey('venues.id'))
  venue = db.relationship('Venue')


  def __init__(self, fb_json):
    self.id              = fb_json['id']
    self.name            = fb_json['name']
    self.category        = fb_json['category']
    self.distance        = fb_json['distance']
    self.attending       = fb_json['stats']['attending']
    self.noreply         = fb_json['stats']['noreply']
    self.declined        = fb_json['stats']['declined']
    self.maybe           = fb_json['stats']['maybe']
    self.description     = fb_json['description']
    self.start_time      = fb_json['start_time']
    self.end_time        = fb_json['end_time']
    self.profile_picture = fb_json['profile_picture']
    self.cover_picture   = fb_json['cover_picture']
    self.time_from_now   = fb_json['time_from_now']
    self.type            = fb_json['type']
    self.venue_id        = fb_json['venue']['id']


class EventSchema(ModelSchema):
  class Meta:
    model = Event
