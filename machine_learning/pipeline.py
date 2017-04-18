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

  def train(self, train_set):
    """Polynomial interpolation of degree 2 (quadratic regression)."""
    self.sklearn_model = make_pipeline(PolynomialFeatures(3), Ridge())
    X, y = train_set[:, 0], train_set[:, 1]
    X = X.reshape(-1, 1)
    results = self.sklearn_model.fit(X, y)
    return results

  def test(self, test_set):
    """Output of quadratic regression model."""
    if not self.sklearn_model:
      raise Exception('Model has not been trained yet.')
    return self.sklearn_model.predict(test_set.reshape(-1, 1))

  def find_peak(self, test_set):
    """
    Finds peak using first derivative test.
    Returns tuple (t, v) representing the peak time and peak value.
    """
    test_values = self.test(test_set)
    derivs = [(i, test_values[i] - test_values[i-1]) for i in xrange(1, len(test_values))]
    sorted_derivs = sorted(derivs, key=lambda t:math.fabs(t[1])) # This yields derivatives with smallest absolute value
    index_of_peak = sorted_derivs[0][0]
    return (index_of_peak, test_values[index_of_peak])

  def __init__(self):
    self.sklearn_model = None

class TimeLocationPair:
    """ Struct containing time, location, attendance """

    def __init__(self, time, venue_id, attendance):
        self.time = time
        self.venue_id = venue_id
        self.attendance = attendance

    def to_json(self):
        return json.dumps({
            "venue_id": self.venue_id,
            "time": self.time,
            "attendance": self.attendance
        })

def top_k_recommendations(events, k=10):

    # Helper function

    def time_model_data(events):
        """Returns a training set for TimeModel."""

        def _get_hour(time_string):
          date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
          return date_time.hour + (date_time.minute / 60.0)

        attendance = [event.attending for event in events]
        time = [_get_hour(event.start_time) for event in events if _get_hour(event.start_time) >= 8]
        attendance_time = zip(time, attendance)
        return np.asarray(attendance_time)

    # Step 1: Group events by venue

    venues_to_events = defaultdict(list)
    for event in events:
        venues_to_events[event.venue.id].append(event)

    # Step 2: Create time models for each event group

    venues_to_models = {}
    for venue_id in venues_to_events:
        t = TimeModel()
        t.train(time_model_data(venues_to_events[venue_id]))
        venues_to_models[venue_id] = t

    # Step 3: Find peaks of models (yielding time-location pairs)

    time_location_pairs = []
    for venue_id in venues_to_models:
        model = venues_to_models[venue_id]
        synthetic_test_data = np.asarray([i/4 for i in xrange(0, 24*4)])
        peak_time, peak_value = t.find_peak(t.test(synthetic_test_data))
        time_location_pairs.append(TimeLocationPair(
            venue_id=venue_id,
            time=peak_time,
            attendance=peak_value
        ))

    # Step 4: Output top time-location pairs

    sorted_pairs = sorted(time_location_pairs, key=lambda t: t.attendance, reverse=True)
    return [pair.to_json() for pair in sorted_pairs[:k]]


if __name__ == "__main__":
    print top_k_recommendations(Event.query.all())
