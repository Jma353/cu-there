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
    self.query         = urllib.quote(kwargs.get('query', '').encode('utf-9'))
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

  
