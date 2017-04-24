# Predictive models for event attendance

from collections import defaultdict
from datetime import datetime
import json
import math
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from app.events.models.event import Event

class TimeModel(object):
  """
  Predicts event attendance based on event time.
  Attempts to fit time-attendance relationship to a polynomial of degree 2
  (with roots at the lowest-attendance times and vertex at the
  highest-attendance time).
  """

  def __init__(self):
    self.hour_model = None
    self.day_model = None
    
  def train_model(self, model, train_set):
    """Polynomial interpolation of degree 2 (quadratic regression)."""
    model = make_pipeline(PolynomialFeatures(3), Ridge())
    X, y = train_set[:, 0], train_set[:, 1]
    X = X.reshape(-1, 1)
    results = model.fit(X, y)
    return results

  def hour_train(self, train_set):
    self.hour_model = self.train_model(self.hour_model, train_set)
    return self.hour_model
    
  def day_train(self, train_set):
    self.day_model = self.train_model(self.day_model, train_set)
    return self.day_model

  def test_model(self, model, test_set):
    """Output of quadratic regression model."""
    if not model:
      return [0]*len(test_set)
    return model.predict(test_set.reshape(-1, 1))

  def hour_test(self, test_set):
    return self.test_model(self.hour_model, test_set)
    
  def day_test(self, test_set):
    return self.test_model(self.day_model, test_set)

  def find_model_peak(self, model, test_set):
    """
    Finds peak using first derivative test.
    Returns tuple (t, v) representing the peak time and peak value.
    """
    test_values = self.test_model(model, test_set)
    derivs = [(i, test_values[i] - test_values[i-1]) for i in xrange(1, len(test_values))]
    sorted_derivs = sorted(derivs, key=lambda t:math.fabs(t[1])) # This yields derivatives with smallest absolute value
    index_of_peak = sorted_derivs[0][0]
    return (index_of_peak, test_values[index_of_peak])
    
  def find_hour_peak(self, test_set):
    return self.find_model_peak(self.hour_model, test_set)
    
  def find_day_of_month_peak(self, test_set):
    return self.find_model_peak(self.day_model, test_set)

class TimeLocationPair:
  """ Struct containing time, location, attendance """

  def __init__(self, time, day_of_month, venue_id, attendance):
    self.time = time
    self.day_of_month = day_of_month
    self.venue_id = venue_id
    self.attendance = attendance

  def to_dict(self):
    return {
      "venue_id": self.venue_id,
      "time": self.time,
      "day_of_month": self.day_of_month,
      "attendance": self.attendance
    }

def top_k_recommendations(events, k=10):
  # Helper function

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

    def _get_hour(time_string):
      date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
      return date_time.hour + (date_time.minute / 60.0)

    return train_data(events, _get_hour)
    
  def day_model_data(events):
    """Returns a training set for the day-of-month component of TimeModel."""
    
    def _get_day(time_string):
      date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
      return date_time.day
      
    return train_data(events, _get_day)

  # Step 1: Group events by venue

  venues_to_events = defaultdict(list)
  for event in events:
    venues_to_events[event.venue.id].append(event)

  # Step 2: Create time models for each event group

  venues_to_models = {}
  for venue_id in venues_to_events:
    t = TimeModel()
    hour_train_data = hour_model_data(venues_to_events[venue_id])
    day_train_data = day_model_data(venues_to_events[venue_id])
    if hour_train_data != [] or day_train_data != []:
      if hour_train_data != []:
        t.hour_train(hour_train_data)
      if day_train_data != []:
        t.day_train(day_train_data)
      venues_to_models[venue_id] = t

  # Step 3: Find peaks of models (yielding time-location pairs)

  time_location_pairs = []
  for venue_id in venues_to_models:
    t = venues_to_models[venue_id]
    synthetic_time_data = np.asarray([i for i in xrange(0, 24)])
    synthetic_day_data = np.asarray([i for i in xrange(0, 31)])
    peak_time, peak_time_value = t.find_hour_peak(synthetic_time_data)
    peak_day, peak_day_value = t.find_day_of_month_peak(synthetic_day_data)
    time_location_pairs.append(TimeLocationPair(
      venue_id=venue_id,
      time=peak_time,
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
