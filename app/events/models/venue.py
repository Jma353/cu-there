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
    self.city            = fb_json['location']['city']
    self.zip             = fb_json['location']['zip']
    self.country         = fb_json['location']['country']
    self.longitude       = fb_json['location']['longitude']
    self.latitude        = fb_json['location']['latitude']
    self.state           = fb_json['location']['state']
    self.street          = fb_json['location']['street']
    self.emails          = '' if fb_json['emails'] is None else ';'.join(fb_json['emails'])

class VenueSchema(ModelSchema):
  class Meta:
    model = Venue 
