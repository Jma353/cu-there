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
    the_venue = Venue(v)
    result = Venue.query.get(the_venue.id)
    if result is None: db.session.add(the_venue)

  # Add all events
  for e in events:
    the_event = Event(e)
    result = Event.query.get(the_event.id)
    if result is None: db.session.add(the_event)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print e


if __name__ == '__main__':
  if len(sys.argv) < 2: raise
  store_venues(sys.argv[1])
