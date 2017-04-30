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

class Recommendation:
  """ 
  Struct containing recommendations for times, venues, tags, etc.
  """

  def __init__(self, **kwargs):
    """
    Initializes internal data structures.
    """
    self.times = []
    self.time_graphs = []
    self.venue_ids = []
    self.venue_events = []
    self.tags = []
    self.features = []

  def add_time(self, peak_time, time_graph):
    """
    Adds a peak time and the time graph it came from.
    :param peak_time: an int
    :param time_graph: a list of lists. first list: x values, second list: y values
    """
    self.times.append(peak_time)
    self.time_graphs.append(time_graph)
    
  def add_venue(self, venue_id, events):
    """
    Adds a venue and the events that contributed to that venue being recommended.
    :param venue_id: a string
    :param events: a list of event names
    """
    self.venue_ids.append(venue_id)
    self.venue_events.append(events)
    
  def add_tag(self, tag):
    """
    Adds a tag.
    """
    self.tags.append(tag)

  def add_feature(self, feature_name):
    """
    Adds a feature.
    """
    self.features.append(feature_name)
    
  def get_venue_ids(self):
    return self.venue_ids
    
  def get_times(self):
    return self.times
    
  def get_features(self):
    return self.features

  def to_dict(self):
    return {
      'times': [{
        'peak': self.times[i],
        'graph': {
          'x': self.time_graphs[i][0],
          'y': self.time_graphs[i][1]
        }
      } for i in xrange(0, len(self.times))],
      'venues': [{
        'id': self.venue_ids[i],
        'events': self.venue_events[i]
      } for i in xrange(0, len(self.venue_ids))],
      'tags': self.tags,
      'features': self.features
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

  # Step 3: Find peaks of models

  time_location_pairs = []
  rec = Recommendation()
  
  for venue_id in venues_to_models:
    hour_model = venues_to_models[venue_id]
    synthetic_time_data = np.asarray([i for i in xrange(0, 24)])
    peak_time, peak_time_value = hour_model.find_peak(synthetic_time_data)
    model_graph = hour_model.generate_graph(synthetic_time_data)

    rec.add_venue(venue_id, venues_to_events[venue_id])
    rec.add_time(peak_time, model_graph)

  # Step 4: Meta-features and tag recommendations
  
  m = MetadataModel(events)
  features_coefs = m.features_coefs()
  
  # For now, let's return the top three features. We can play around with this or generate a number programmatically
  
  top_three_feature_names = sorted(features_coefs.keys(), key=features_coefs.get, reverse=True)[:3]
  for feature_name in top_three_feature_names:
    rec.add_feature(feature_name)
  
  return rec

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
    rec = top_k_recommendations(events)

    # print recs
    print "Top venues:"
    print
    for venue_id in rec.get_venue_ids():
      print Venue.query.filter_by(id=venue_id).first().name
    print
    for time in rec.get_times():
      print time
    print
    print "Top features:"
    print
    for feature_name in rec.get_features():
      print feature_name