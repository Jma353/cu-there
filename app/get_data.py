from event_search import EventSearch
from constants import *
import time
import json
import os

DIRECTORY = '../results'

def get_events_since(since):

  # Get all the weeks we're querying on
  now = int(round(time.time()))
  then = since
  weeks = []
  while then < now-WEEK:
    weeks.append((then, then+WEEK))
    then += WEEK
  if then < now:
    weeks.append((then, now))

  # Grab results
  results = dict()
  for w in weeks:

    search = EventSearch(
      distance=12000,
      lat=LATITUDE,
      lng=LONGITUDE,
      since=w[0],
      until=w[1]).search()

    # Accumulate
    for e in search['events']:
      results[e['id']] = e

    # Sleep accordingly
    time.sleep(4)

    print "Grabbed the events in week " + str(w)

  # Dictionary to list
  results = [results[k] for k in results.keys()]

  # Store
  secs = str(int(round(time.time())))
  if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
  with open(DIRECTORY + '/' + secs + '.json', 'w') as outfile:
    json.dump(results, outfile)


# Get events from specific duration
get_events_since(int(round(time.time())) - 7 * YEAR)
