# Predictive models for event attendance

from collections import defaultdict
import json
import math
import numpy as np

from app.events.models.event import Event, EventSchema
from models.metadata import MetadataModel
from models.time import TimeModel
from models.tags import TagModel
import utils

event_schema = EventSchema()

class TimeLocationPair:
  """ Struct containing time, location, attendance """

  def __init__(self, **kwargs):
    # Grab event information
    self.time = kwargs.get('time')
    self.time_graph = kwargs.get('time_graph')
    self.venue_id = kwargs.get('venue_id')
    self.attendance = kwargs.get('attendance')
    self.events = kwargs.get('events')

  def to_dict(self):
    return {
      "venue_id": self.venue_id,
      "time": self.time,
      "time_graph": self.time_graph,
      "attendance": self.attendance,
      "events": [event_schema.dump(e).data for e in self.events]
    }

def top_k_recommendations(events, k=10):

  def _average_attendance_by_time(attendance_time):
    """ 
    Helper function for returning average attendance for each discrete time value. 
    """
    buckets = defaultdict(list)

    for i in xrange(8, 24):
      for pair in attendance_time:
        if pair[0] == i:
          buckets[i].append(pair[1])
    mean_buckets = defaultdict(int)

    for i in xrange(8, 24):
      if len(buckets[i]) > 0:
        mean_buckets[i] = sum(buckets[i])/len(buckets[i])

    # We now have the max attendance for each time

    mean_attendance_time = zip(mean_buckets.keys(), mean_buckets.values())
    return np.asarray(mean_attendance_time)

  def train_data(events, func):
    """ 
    Creates training data for attendance vs. `func` where `func` is a function
    of the event time. 
    """
    attendance = [event.attending for event in events]
    time = [func(event.start_time) for event in events]
    attendance_time = zip(time, attendance)
    return _average_attendance_by_time(attendance_time)

  def hour_model_data(events):
    """
    Returns a training set for the hour component of TimeModel.
    """
    return train_data(events, utils.get_hour)

  # Step 1: Group events by venue

  for i in xrange(0, len(events)):
    events[i].attending = events[i].attending*math.e**(-1*i)

  venues_to_events = defaultdict(list)
  for event in events:
    venues_to_events[event.venue.id].append(event)

  event_lengths = [len(venues_to_events[venue_id]) for venue_id in venues_to_events]
  median_event_length = sorted(event_lengths)[len(event_lengths)/2]

  for venue_id in venues_to_events:
    events = venues_to_events[venue_id]
    for event in events:
      event.attending *= math.fabs((len(events) - median_event_length) + 0.1)**(-0.5)

  # Step 2: Create time models for each event group

  venues_to_models = {}
  for venue_id in venues_to_events:
    hour_model = TimeModel(feature_func=utils.get_hour)
    hour_train_data = hour_model_data(venues_to_events[venue_id])
    if hour_train_data != []:
      hour_model.train(hour_train_data, venues_to_events[venue_id])
    venues_to_models[venue_id] = hour_model

  # Step 3: Find peaks of models (yielding time-location pairs)

  time_location_pairs = []
  for venue_id in venues_to_models:
    hour_model = venues_to_models[venue_id]
    synthetic_time_data = np.asarray([i for i in xrange(0, 24)])
    peak_time, peak_time_value = hour_model.find_peak(synthetic_time_data)
    model_graph = hour_model.generate_graph(synthetic_time_data)

    time_location_pairs.append(TimeLocationPair(
      venue_id     = venue_id,
      time         = peak_time,
      time_graph   = model_graph,
      events  = [event for event in venues_to_events[venue_id]],
      attendance   = peak_time_value
    ))

  # Step 4: Output top time-location pairs

  sorted_pairs = sorted(time_location_pairs, key=lambda t: t.attendance, reverse=True)
  return [pair.to_dict() for pair in sorted_pairs[:k]]

if __name__ == "__main__":
  # Testing
  from app.events.models.venue import Venue

  while True:
    print "Enter query:"
    print
    query = str(raw_input(">>> "))
    print

    events = Event.query.all()
    events = [event for event in events if query in event.name.lower()]
    recs = top_k_recommendations(events)

    # print recs
    print "Top location-time pairs for the {} events retrieved:".format(len(events))
    print
    for rec in recs:
      print "{} at {}:00. Predicted attendance: {}\nRecommended because of: {}".format(
        Venue.query.filter_by(id=rec["venue_id"]).first().name,
        rec["time"],
        rec["attendance"],
        ", ".join([name for name in rec["event_names"]])
      )
    print
