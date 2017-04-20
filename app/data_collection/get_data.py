import time
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.facebook_event_search import FacebookEventSearch
from app.constants import *

DIRECTORY = './results'

def get_events_since(**kwargs):
  # Grab arguments
  since    = kwargs.get('since')
  until    = kwargs.get('until')
  interval = kwargs.get('interval')
  lat      = kwargs.get('lat')
  lng      = kwargs.get('lng')
  print 'From: ' + str(since)
  print 'Until: ' + str(until)
  print 'Using interval: ' + str(interval)
  print 'Latitude: ' + str(lat)
  print 'Longitude: ' + str(lng)

  then = since
  spans = []
  while then < now-interval:
    spans.append((then, then+interval))
    then += interval
  if then < until:
    spans.append((then, now))

  # Grab results
  results = dict()
  for s in spans:

    search = FacebookEventSearch(
      distance=FB_RADIUS,
      lat=lat,
      lng=lng,
      since=s[0],
      until=s[1]).search()

    # Accumulate
    for e in search['events']:
      results[e['id']] = e

    # Sleep accordingly
    time.sleep(3)

    print "Grabbed the events in span " + str(s)

  # Dictionary to list
  results = [results[k] for k in results.keys()]
  print results

  # Store
  secs = str(int(round(time.time())))
  if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
  with open(DIRECTORY + '/' + secs + '.json', 'w') as outfile:
    json.dump(results, outfile)


if __name__ == "__main__":
  # RN
  now = int(round(time.time()))

  # Grab arguments
  from_years = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YEARS
  to_years   = float(sys.argv[2]) if len(sys.argv) > 2 else 0
  lat        = float(sys.argv[3]) if len(sys.argv) > 3 else LATITUDE
  lng        = float(sys.argv[4]) if len(sys.argv) > 4 else LONGITUDE

  # Run it
  get_events_since(
    since=now-from_years*YEAR,
    until=now-to_years*YEAR,
    interval=DAY,
    lat=lat,
    lng=lng
  )
