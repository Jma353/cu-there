from eventbrite import Eventbrite
from constants import *
import datetime
import urllib
import time
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
    self.distance = str(kwargs.get('distance', 25)) + 'mi'
    self.query = urllib.quote(kwargs.get('query', '').encode('utf-8'))
    self.sort = kwargs.get('sort', None) if kwargs.get('sort', 'venue') in allowed_sorts else 'best'
    self.since = datetime.datetime.fromtimestamp(kwargs.get('since', int(round(time.time())) - 10 * YEAR)).strftime(datetime_str)
    self.until = datetime.datetime.fromtimestamp(kwargs.get('until', int(round(time.time())))).strftime(datetime_str)

  def search(self):
    """Overall search workhorse function"""

    # Parameters according to:
    # https://www.eventbrite.com/developer/v3/endpoints/events/
    params = {
      'q': self.query,
      'sort_by': self.sort,
      'start_date.range_start': self.since,
      'start_date.range_end': self.until,
      'include_unavailable_events': True
    }

    if (self.distance is not None and
        self.latitude is not None and
        self.longitude is not None): params['location.within'] = self.distance
    if self.latitude is not None: params['location.latitude'] = self.latitude
    if self.longitude is not None: params['location.longitude'] = self.longitude

    query_url = '/events/search/?' + urllib.urlencode(params)
    print params
    return self.api.get(query_url)


print EventbriteEventSearch(query='Cornell University').search()
