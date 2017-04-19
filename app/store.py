from app.events.models.event import Event
from app.events.models.venue import Venue
import json
import sys

def store_venues(f, db):
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
      db.session.commit()
    except Exception as e:
      db.session.rollback()


  # Add all events
  for e in events:
    try:
      db.session.add(Event(e))
      db.session.commit()
    except Exception as e:
      db.session.rollback()


if __name__ == '__main__':
  if len(sys.argv) < 2: raise
  store_venues(sys.argv[1])
