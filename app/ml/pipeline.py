# Predictive models for event attendance

from collections import defaultdict
import json
import math
import numpy as np

from app.events.models.event import Event
import polyfit
from utils import *

class QuadraticModel(object):
  """ Model for a polynomial of degree 2.
      feature_func is the function used to extract the independent variable from an event
      (for example, get_hour).

      Contains a train, test, and find_peak function.
  """
  model = None
  feature_func = None
  events = []

  def __init__(self, feature_func):
    self.feature_func = feature_func
    self.events = []

  def train(self, train_set, events):
    """ Trains model. """
    if self.events == []:
      self.events = events
    self.model = polyfit.create_fit(train_set)
    return self.model

  def test(self, test_set):
    """ Tests model. """
    if not self.model:
      return [0]*len(test_set)
    return self.model(test_set.reshape(-1, 1))

  def generate_graph(self, synthetic_data):
    test_values = self.test(synthetic_data)
    try:
      return [list(synthetic_data), [list(i)[0] for i in list(test_values)]]
    except TypeError:
      return []

  def find_peak(self, test_set):
    """
    Finds peak using first derivative test.
    Returns tuple (t, v) representing the peak time and peak value.
    """
    test_values = self.test(test_set)

    # TESTING CODE - do not uncomment in production
    #import matplotlib.pyplot as plt
    #plt.scatter([self.feature_func(event.start_time) for event in self.events], [event.attending for event in self.events])
    #plt.plot(test_set, test_values)
    #plt.show()

    derivs = [(i, test_values[i] - test_values[i-1]) for i in xrange(1, len(test_values))]
    sorted_derivs = sorted(derivs, key=lambda t:math.fabs(t[1])) # This yields derivatives with smallest absolute value
    index_of_peak = sorted_derivs[0][0]
    return (index_of_peak, test_values[index_of_peak])

class EventMetadataModel:
  """
  Model for event meta-features
  """
  model = None
  
  def __init__(self, events):
    pass

class TimeLocationPair:
  """ Struct containing time, location, attendance """

  def __init__(self, time, time_graph, day_of_month, venue_id, attendance):
    self.time = time
    self.time_graph = time_graph
    self.day_of_month = day_of_month
    self.venue_id = venue_id
    self.attendance = attendance

  def to_dict(self):
    return {
      "venue_id": self.venue_id,
      "time": self.time,
      "time_graph": self.time_graph,
      "day_of_month": self.day_of_month,
      "attendance": self.attendance
    }

def top_k_recommendations(events, k=10):

  def _bucketify(attendance_time):
    """ Helper function for returning average attendance for each discrete time value. """
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
    """ Creates training data for attendance vs. `func` where `func` is a function
        of the event time. """
    attendance = [event.attending for event in events]
    time = [func(event.start_time) for event in events]
    attendance_time = zip(time, attendance)
    return _bucketify(attendance_time)

  def hour_model_data(events):
    """Returns a training set for the hour component of TimeModel."""
    return train_data(events, get_hour)

  def day_model_data(events):
    """Returns a training set for the day-of-month component of TimeModel."""
    return train_data(events, get_day)

  # Step 1: Group events by venue

  for i in xrange(0, len(events)):
    events[i].attending = events[i].attending*math.e**(-1*i)

  venues_to_events = defaultdict(list)
  for event in events:
    venues_to_events[event.venue.id].append(event)

  for venue_id in venues_to_events:
    events = venues_to_events[venue_id]
    for event in events:
      event.attending *= (len(events))**(-0.5)

  # Step 2: Create time models for each event group

  venues_to_models = {}
  for venue_id in venues_to_events:
    hour_model = QuadraticModel(feature_func=get_hour)
    day_model = QuadraticModel(feature_func=get_day)
    hour_train_data = hour_model_data(venues_to_events[venue_id])
    day_train_data = day_model_data(venues_to_events[venue_id])
    if hour_train_data != [] or day_train_data != []:
      if hour_train_data != []:
        hour_model.train(hour_train_data, venues_to_events[venue_id])
      if day_train_data != []:
        day_model.train(day_train_data, venues_to_events[venue_id])
      venues_to_models[venue_id] = {"hour": hour_model, "day": day_model}

  # Step 3: Find peaks of models (yielding time-location pairs)

  time_location_pairs = []
  for venue_id in venues_to_models:
    model_bundle = venues_to_models[venue_id]
    hour_model, day_model = model_bundle["hour"], model_bundle["day"]

    synthetic_time_data = np.asarray([i for i in xrange(0, 24)])
    synthetic_day_data = np.asarray([i for i in xrange(0, 31)])

    peak_time, peak_time_value = hour_model.find_peak(synthetic_time_data)
    peak_day, peak_day_value = day_model.find_peak(synthetic_day_data)

    model_graph = hour_model.generate_graph(synthetic_time_data)

    time_location_pairs.append(TimeLocationPair(
      venue_id=venue_id,
      time=peak_time,
      time_graph=model_graph,
      day_of_month=peak_day,
      attendance=(peak_time_value + peak_day_value)/2
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
      print "{} on day {} at {}:00. Predicted attendance: {}".format(
        Venue.query.filter_by(id=rec["venue_id"]).first().name,
        rec["day_of_month"],
        rec["time"],
        rec["attendance"]
      )
    print
