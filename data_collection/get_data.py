from app.facebook_event_search import FacebookEventSearch
from app.constants import *
import time
import json
import os
import sys

DIRECTORY = '../results'

def get_events_since(since):

  # Get all the spans of time we're querying on
  now = int(round(time.time()))
  then = since
  spans = []
  interval = DAY
  while then < now-interval:
    spans.append((then, then+WEEK))
    then += interval
  if then < now:
    spans.append((then, now))

  # Grab results
  results = dict()
  for s in spans:

    search = FacebookEventSearch(
      distance=RADIUS,
      lat=LATITUDE,
      lng=LONGITUDE,
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
  years = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_YEARS
  # Get events from specific duration
  get_events_since(int(round(time.time())) - years * YEAR)
