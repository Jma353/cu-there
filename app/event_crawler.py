from event_search import EventSearch
import json
import time
import os

class EventCrawler(object):
  """Crawls events"""

  def __init__(self, distance, directory):
    """Constructor"""
    self.driver = EventSearch(
      lat       = float(os.environ['LATITUDE']),
      lng       = float(os.environ['LONGITUDE']),
      distance  = distance,
      sort      = 'distance')
    self.directory = directory # Where to store results

  def events_in_json(self):
    """Grab events and store in JSON w/timestamp"""
    results = self.driver.search()
    secs = str(int(round(time.time())))
    if not os.path.exists(self.directory):
      os.makedirs(self.directory)
    with open(self.directory + '/' + secs + '.json', 'w') as outfile:
      json.dump(results, outfile)


# Dry run
crawler = EventCrawler(1000, '../results')
crawler.events_in_json()
