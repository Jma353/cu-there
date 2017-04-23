from app import db
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
  id_to_venue = {d['venue']['id']:d['venue'] for d in data}
  venues = [id_to_venue[k] for k in id_to_venue.keys()]
  events = data

  # Grab current IDs
  current_venue_ids = set([v.id for v in Venue.query.all()])
  current_event_ids = set([e.id for e in Event.query.all()])

  # Add all venues
  for v in venues:
    the_venue = Venue(v)
    if (the_venue.id not in current_venue_ids):
      db.session.add(the_venue)

  # Add all events
  for e in events:
    the_event = Event(e)
    if (the_event.id not in current_event_ids):
      db.session.add(the_event)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print e


if __name__ == '__main__':
  if len(sys.argv) < 2: raise
  store_venues(sys.argv[1], db)
