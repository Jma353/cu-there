from . import *

class Venue(Base):
  __tablename__ = 'venues'
  id              = db.Column(db.String(), primary_key=True)
  about           = db.Column(db.Text())
  name            = db.Column(db.String())
  profile_picture = db.Column(db.String(2000))
  cover_picture   = db.Column(db.String(2000))
  city            = db.Column(db.String())
  zip             = db.Column(db.String())
  country         = db.Column(db.String())
  longitude       = db.Column(db.Float())
  latitude        = db.Column(db.Float())
  state           = db.Column(db.String())
  street          = db.Column(db.String())
  emails          = db.Column(db.Text())

  def __init__(self, fb_json):
    """
    Constructor from FB JSON
    """
    self.id              = fb_json.get('id')
    self.about           = fb_json.get('about')
    self.name            = fb_json.get('name')
    self.profile_picture = fb_json.get('profile_picture')
    self.cover_picture   = fb_json.get('cover_picture')
    self.city            = fb_json.get('location', {}).get('city')
    self.zip             = fb_json.get('location', {}).get('zip')
    self.country         = fb_json.get('location', {}).get('country')
    self.longitude       = fb_json.get('location', {}).get('longitude')
    self.latitude        = fb_json.get('location', {}).get('latitude')
    self.state           = fb_json.get('location', {}).get('state')
    self.street          = fb_json.get('location', {}).get('street')
    self.emails          = ';'.join((fb_json.get('emails') or []))

class VenueSchema(ModelSchema):
  class Meta:
    model = Venue
