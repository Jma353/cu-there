# Several functions for building & executing queries on the data
# modeled in this module

from event import Event
from venue import Venue
from sqlalchemy.orm import joinedload

def get_events(event_ids):
  """
  Returns a list of events of said id's
  """
  return [
    Event.query.options(joinedload('venue')).get(i)
    for i in event_ids
  ]

def get_venues(venue_ids):
  """
  Returns a list of venues of said id's
  """
  return [Venue.query.get(i) for i in venue_ids]
