import requests as r
import dateutil as du
import urllib
import os
import utils
import datetime
import haversine

class EventSearch(object):
  """
  Event search driver by name, location, etc.

  Based heavily off tobilg's 'facebook-events-by-location-core' node.js
  driver, found here: https://goo.gl/zVA8F5
  """

  def __init__(self, **kwargs):
    """Constructor"""
    self.allowed_sorts = ['time', 'distance', 'venue', 'popularity']
    self.latitude      = kwargs.get('lat', None)
    self.longitude     = kwargs.get('lng', None)
    self.distance      = kwargs.get('distance', 50)
    self.access_token  = kwargs.get('access_token', utils.get_app_access_token())
    self.query         = urllib.quote(kwargs.get('query', '').encode('utf-8'))
    self.sort          = kwargs.get('sort', 'venue') if kwargs.get('sort', 'venue') in self.allowed_sorts else None
    self.version       = kwargs.get('version', 'v2.7')
    self.since         = kwargs.get('since', int(datetime.datetime.now().microsecond / 1000.0))
    self.until         = kwargs.get('until', None)


  def calculate_start_time_diff(self, curr_time, date_str):
    """Difference based on curr_time and provided date string"""
    return (du.parser.parse(date_str).microsecond - (curr_time * 1000)) / 1000.0


  def compare_venue(self, a, b):
    """Comparable venues of a and b"""
    a_name = a['venue']['name']; b_name = b['venue']['name']
    if a_name < b_name:
      return -1
    elif a_name > b_name:
      return 1
    else:
      return 0


  def compare_time_from_now(self, a, b):
    """Comparable times of a and b"""
    a_dist = int(a['distance'])
    b_dist = int(b['distance'])
    if a_dist < b_dist:
      return -1
    elif a_dist > b_dist:
      return 1
    else:
      return 0


  def compare_popularity(self, a, b):
    """Comparable popularity of a and b"""
    a_score = a['stats']['attending'] + a['stats']['maybe'] / 2.0
    b_score = b['stats']['attending'] + b['stats']['maybe'] / 2.0
    if a_score < b_score:
      return -1
    elif a_score > b_score:
      return 1
    else:
      return 0


  def haversine_distance(self, coords1, coords2, is_miles):
    """
    Haversine distance (https://goo.gl/VdQZp4) between `coords1`
    and `coords2`.

    NOTE: coords{1,2} is of the form: [latitude, longitude] (list or tuple)
    """
    return haversine.haversine(tuple(coords1), tuple(coords2), miles=is_miles)


  def search(self):
    """Overall search function"""

    if (self.latitude is None or self.longitude is None):
      raise Exception('Please specify both a latitude and longitude')

    if (self.access_token == '' or self.access_token is None):
      raise Exception('Please specify a valid access token')

    # Book-keeping
    id_limit = 50 # Only 50 per /?ids= call allowed by FB
    curr_time = int(datetime.datetime.now().microsecond / 1000.0)
    venues_count = 0
    venues_with_events = 0
    events_count = 0

    # Initial request info
    place_params = {
      'type': 'place',
      'q': self.query,
      'center': str(self.latitude) + ',' + str(self.longitude),
      'distance': self.distance,
      'limit': 1000,
      'fields': 'id',
      'access_token': self.access_token
    }
    place_url = ('https://graph.facebook.com/' + self.version + '/search?' +
      urllib.urlencode(place_params))

    places = r.get(place_url)

    # TODO - get events from places
    return places.json()


# Hand-testing
driver = EventSearch(lat=40.710803, lng=-73.964040,distance=100)
print driver.search()
