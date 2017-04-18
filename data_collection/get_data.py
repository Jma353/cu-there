from app.facebook_event_search import FacebookEventSearch
from app.constants import *
import time
import json
import os
import sys

DIRECTORY = './results'

def get_events_since(**kwargs):
  # Grab arguments
  since    = kwargs.get('since')
  interval = kwargs.get('interval')
  lat      = kwargs.get('lat')
  lng      = kwargs.get('lng')

  # Get all the spans of time we're querying on
  now = int(round(time.time()))
  then = since
  spans = []
  while then < now-interval:
    spans.append((then, then+WEEK))
    then += interval
  if then < now:
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
  to_years   = float(sys.argv[2]) if len(sys.argv) > 2 else now
  lat        = float(sys.argv[2]) if len(sys.argv) > 3 else LATITUDE
  lng        = float(sys.argv[3]) if len(sys.argv) > 4 else LONGITUDE

  # Run it
  get_events_since(
    since=now-from_years*YEAR,
    until=now-to_years*YEAR,
    interval=DAY,
    lat=lat,
    lng=lng
  )
