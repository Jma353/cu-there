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
    self.id              = fb_json.get('id')
    self.name            = fb_json.get('name')
    self.category        = fb_json.get('category')
    self.distance        = fb_json.get('distance')
    self.attending       = fb_json.get('stats', {}).get('attending')
    self.noreply         = fb_json.get('stats', {}).get('noreply')
    self.declined        = fb_json.get('stats', {}).get('declined')
    self.maybe           = fb_json.get('stats', {}).get('maybe')
    self.description     = fb_json.get('description')
    self.start_time      = fb_json.get('start_time')
    self.end_time        = fb_json.get('end_time')
    self.profile_picture = fb_json.get('profile_picture')
    self.cover_picture   = fb_json.get('cover_picture')
    self.time_from_now   = fb_json.get('time_from_now')
    self.type            = fb_json.get('type')
    self.venue_id        = fb_json.get('venue', {}).get('id')

class EventSchema(ModelSchema):
  class Meta:
    model = Event
