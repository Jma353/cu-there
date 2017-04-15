from eventbrite import Eventbrite
import datetime
import urllib
import os

class EventbriteEventSearch(object):
  """
  Eventbrite event search driver by name, location, etc.
  """

  def __init__(self, **kwargs):
    """Constructor"""

    # Allowed sorts
    allowed_sorts = ['date', 'distance', 'best']
    datetime_str = '%Y-%m-%dT%H:%M:%S'

    # API wrapper
    self.api = Eventbrite(os.environ['EVENTBRITE_TOKEN'])

    # Fields we're querying on
    self.latitude = kwargs.get('lat', None)
    self.longitude = kwargs.get('lng', None)
    self.distance = kwargs.get('distance', 10)
    self.query = urllib.quote(kwargs.get('query', '').encode('utf-8'))
    self.sort = kwargs.get('sort', None) if kwargs.get('sort', 'venue') in allowed_sorts else None
    self.since = datetime.datetime.fromtimestamp(kwargs.get('since', int(round(time.time())) - constants.MONTH)).strftime(datetime_str)
    self.until = datetime.datetime.fromtimestamp(kwargs.get('until', int(round(time.time())))).strftime(datetime_str)

  def search(self):
    """Overall search workhorse function"""

    # Parameters according to:
    # https://www.eventbrite.com/developer/v3/endpoints/events/
    params = {
      'q': self.query,
      'sort_by': self.sort,
      'location': {
        'within': self.distance,
        'latitude': self.latitude,
        'longitude': self.longitude
      },
      'start_date': {
        'range_start': self.since,
        'range_end': self.until
      }
    }

    query_url = '/events/search/?' + urllib.urlencode(params)
    return self.api.get(query_url)


# TODO - hand-testing
