from . import *

class User(Base):
  __tablename__ = 'users'

  google_id   = db.Column(db.String(128), nullable=False)
  email       = db.Column(db.String(128), nullable=False, unique=True)
  fname       = db.Column(db.String(128), nullable=False)
  lname       = db.Column(db.String(128), nullable=False)
  picture_url = db.Column(db.String(512), nullable=False)

  def __init__(self, **kwargs):
    self.google_id   = kwargs.get('google_id', None)
    self.email       = kwargs.get('email', None)
    self.fname       = kwargs.get('fname', None)
    self.lname       = kwargs.get('lname', None)
    self.picture_url = kwargs.get('picture_url', None)

  def __repr__(self):
    return str(self.__dict__)



class UserSchema(ModelSchema):
  class Meta:
    model = User
