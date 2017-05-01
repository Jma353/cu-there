import math
import utils

def suggest_pairs(events, times, locations):
  """
  Suggests possible couplings of times and locations.
  Only suggest a location for a given time if an event at that location
  has taken place around that time.
  """
  pairs = []
  for time in times:
    for event in events:
      if math.fabs(time - utils.get_hour(event.start_time)) <= 2 and event.venue_id in locations:
        pairs.append({"time": time, "venue_id": event.venue_id})
  to_add = []
  for pair in pairs:
    to_add.append(True)
  unique_pairs = []
  for i in xrange(0, len(pairs)):
    for j in xrange(i, len(pairs)):
      if i != j and pairs[i]["time"] == pairs[j]["time"] and pairs[i]["venue_id"] == pairs[j]["venue_id"]:
        to_add[j] = False
  for i in xrange(0, len(to_add)):
    if to_add[i]:
      unique_pairs.append(pairs[i])
  return unique_pairs