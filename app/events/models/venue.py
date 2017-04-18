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
  longitude       = db.Column(db.String())
  latitude        = db.Column(db.String())
  state           = db.Column(db.String())
  street          = db.Column(db.String())
  cover_picture   = db.Column(db.String(2000))
  emails          = db.Column(db.Text())

  def __init__(self, fb_json):
    """
    Constructor from FB JSON
    """
    self.id              = fb_json['id']
    self.about           = fb_json['about']
    self.name            = fb_json['name']
    self.profile_picture = fb_json['profile_picture']
    self.cover_picture   = fb_json['cover_picture']
    self.city            = fb_json['city']
    self.zip             = fb_json['zip']
    self.country         = fb_json['country']
    self.longitude       = fb_json['longitude']
    self.latitude        = fb_json['latitude']
    self.state           = fb_json['state']
    self.street          = fb_json['street']
    self.cover_picture   = fb_json['cover_picture']
    self.emails          = '' if fb_json['emails'] is None else ';'.join(fb_json['emails'])
