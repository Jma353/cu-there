# Several functions for building & executing queries on the data
# modeled in this module

from event import Event
from sqlalchemy.orm import joinedload

def get_events(event_ids):
  """
  Builds an event id query and return a list of events
  with said id's
  """
  return [
    Event.query.options(joinedload('venue')).get(i)
    for i in event_ids
  ]
