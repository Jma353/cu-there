from app.events.models.event import Event
from app.events.models.venue import Venue
from app import db

def store_venues(f):
  """
  Store venues based on a file name `f`
  """
  data = []
  with open(f) as data_file:
    data.extend(json.load(data_file))

  # Grab venues and events
  venues = [d['venue'] for d in data]
  events = data

  # Add all venues
  for v in venues:
    try:
      db.session.add(Venue(v))
      db.commit()
    except Exception e:
      print e


  # Add all events
  for e in events:
    try:
      db.session.add(Event(e))
      db.commit()
    except Exception e:
      print e
