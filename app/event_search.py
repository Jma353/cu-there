import requests as r
import urllib
import os
import utils
import time
import haversine
from dateutil import parser

class EventSearch(object):
  """
  Event search driver by name, location, etc.

  Based heavily off tobilg's 'facebook-events-by-location-core' node.js
  driver, found here: https://goo.gl/zVA8F5
  """

  def __init__(self, **kwargs):
    """Constructor"""

    # Listed sorts w/matching functions
    self.allowed_sorts = {
      'time' : self.compare_time_from_now,
      'distance': self.compare_distance,
      'venue': self.compare_venue,
      'popularity': self.compare_popularity
    }

    self.latitude      = kwargs.get('lat', None)
    self.longitude     = kwargs.get('lng', None)
    self.distance      = kwargs.get('distance', 500)
    self.access_token  = kwargs.get('access_token', utils.get_app_access_token())
    self.query         = urllib.quote(kwargs.get('query', '').encode('utf-8'))
    self.sort          = kwargs.get('sort', None) if kwargs.get('sort', 'venue') in self.allowed_sorts else None
    self.version       = kwargs.get('version', 'v2.7')
    self.since         = kwargs.get('since', int(round(time.time())) - 2.628e+6) # Events from the last month
    self.until         = kwargs.get('until', None)


  def calculate_start_time_diff(self, curr_time, date_str):
    """Difference based on curr_time and provided date string"""
    return (parser.parse(date_str).microsecond - (curr_time * 1000)) / 1000.0


  def compare_venue(self, a, b):
    """Comparable venues of a and b"""
    a_name = a['venue']['name']; b_name = b['venue']['name']
    if a_name < b_name:
      return -1
    elif a_name > b_name:
      return 1
    else:
      return 0


  def compare_distance(self, a, b):
    """Comparable distance of a and b"""
    a_dist = int(a['distance'])
    b_dist = int(b['distance'])
    if a_dist < b_dist:
      return -1
    elif a_dist > b_dist:
      return 1
    else:
      return 0


  def compare_time_from_now(self, a, b):
    if a['time_from_now'] < b['time_from_now']:
      return -1
    elif a['time_from_now'] > b['time_from_now']:
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


  def haversine_distance(self, coords1, coords2, is_miles=False):
    """
    Haversine distance (https://goo.gl/VdQZp4) between `coords1`
    and `coords2`.

    NOTE: coords{1,2} is of the form: [latitude, longitude] (list or tuple)
    """
    return haversine.haversine(tuple(coords1), tuple(coords2), miles=is_miles)


  def search(self):
    """Overall search workhorse function"""

    if (self.latitude is None or self.longitude is None):
      raise Exception('Please specify both a latitude and longitude')

    if (self.access_token == '' or self.access_token is None):
      raise Exception('Please specify a valid access token')

    # Book-keeping
    id_limit = 50 # Only 50 per /?ids= call allowed by FB
    curr_time = int(round(time.time()))
    venues_count = 0
    events_count = 0

    # Initial places request info
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

    # Grab places and prepare to get events
    places_data = r.get(place_url).json()['data']
    venues_count = len(places_data)

    # Batch places based on FB id_limit
    ids = []
    temp_lst = []
    for place in places_data:
      temp_lst.append(place['id'])
      if len(temp_lst) >= id_limit:
        ids.append(temp_lst)
        temp_lst = []
    if len(ids) == 0:
      ids.append(temp_lst)

    # Inner function to convert a list of
    # ids to a request url for events
    def ids_to_url(id_lst):
      events_fields = [
        'id',
        'type',
        'name',
        'cover.fields(id,source)',
        'picture.type(large)',
        'description',
        'start_time',
        'end_time',
        'category',
        'attending_count',
        'declined_count',
        'maybe_count',
        'noreply_count'
      ]

      fields = [
        'id',
        'name',
        'about',
        'emails',
        'cover.fields(id,source)',
        'picture.type(large)',
        'location',
        'events.fields(' + ','.join(events_fields) + ')'
      ]

      timing = ('.since(' + str(self.since) + ')' +
        ('' if self.until is None else '.until(' + str(self.until) + ')'))

      events_params = {
        'ids': ','.join(id_lst),
        'access_token': self.access_token,
        'fields': ','.join(fields) + timing
      }

      events_url = ('https://graph.facebook.com/' + self.version + '/?' +
        urllib.urlencode(events_params))

      return r.get(events_url).json()

    # Event results
    results = [ids_to_url(id_lst) for id_lst in ids]

    # Inner function to convert a list of
    # of venue result events to a list of
    # well-formatted events
    def venue_to_events(venue):
      venue_events = []
      if 'events' in venue and len(venue['events']['data']) > 0:
        for event in venue['events']['data']:
          event_r                    = dict()
          event_r['id']              = event['id']
          event_r['name']            = event['name']
          event_r['type']            = event['type']
          event_r['cover_picture']   = event['cover']['source'] if 'cover' in event else None
          event_r['profile_picture'] = event['picture']['data']['url'] if 'picture' in event else None
          event_r['description']     = event['description'] if 'description' in event else None
          event_r['start_time']      = event['start_time'] if 'start_time' in event else None
          event_r['end_time']        = event['end_time'] if 'end_time' in event else None
          event_r['time_from_now']   = self.calculate_start_time_diff(curr_time, event['start_time'])
          event_r['category']        = event['category'] if 'category' in event else None
          event_r['distance']        = (self.haversine_distance([venue['location']['latitude'],
                                                                 venue['location']['longitude']],
                                                                [self.latitude, self.longitude]) * 1000
                                                                 if 'location' in venue else None)

          event_r['stats'] = {
            'attending': event['attending_count'],
            'declined': event['declined_count'],
            'maybe': event['maybe_count'],
            'noreply': event['noreply_count']
          }

          event_r['venue'] = {
            'id': venue['id'],
            'name': venue['name'],
            'about': venue['about'] if 'about' in venue else None,
            'emails': venue['emails'] if 'emails' in venue else None,
            'cover_picture': venue['cover']['source'] if 'cover' in venue else None,
            'profile_picture': venue['picture']['data']['url'] if 'picture' in venue else None,
            'location': venue['location'] if 'location' in venue else None
          }

          venue_events.append(event_r)
      return venue_events

    # Grab the events
    events = []
    for result in results:
      for venue_id in result.keys():
        events.extend(venue_to_events(result[venue_id]))
    events_count = len(events)

    # Sort if specified
    if self.sort is not None:
      events.sort(self.allowed_sorts[self.sort])

    # Return events w/metadata
    return {
      'events': events,
      'metadata': { 'venues': venues_count, 'events': events_count }
    }
