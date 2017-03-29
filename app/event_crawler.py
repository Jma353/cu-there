from event_search import EventSearch
import constants
import json
import time
import os

class EventCrawler(object):
  """Crawls events"""

  def __init__(self, **kwargs):
    """Constructor"""
    self.driver = EventSearch(**kwargs)
    self.directory = kwargs.get('directory')

  def events_in_json(self):
    """Grab events and store in JSON w/timestamp"""
    results = self.driver.search()
    secs = str(int(round(time.time())))
    if not os.path.exists(self.directory):
      os.makedirs(self.directory)
    with open(self.directory + '/' + secs + '.json', 'w') as outfile:
      json.dump(results, outfile)

# Dry run
crawler = EventCrawler(
  distance=15000,
  directory='../results',
  lat=constants.LATITUDE,
  lng=constants.LONGITUDE,
  since=int(round(time.time())) - 11 * constants.YEAR)


crawler.events_in_json()
