# Predictive models for event attendance

from collections import defaultdict
import json
import math
import numpy as np

from app import preprocessed
from app.events.models.event import Event, EventSchema
from models.metadata import MetadataModel
from models.time import TimeModel
from models.tags import TagModel
from models.constants import *
import coupling
import topic_regression
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
    self.peak_attendances = []
    self.time_graphs = []
    self.venue_ids = []
    self.venue_events = []
    self.tags = []
    self.features = []

  def add_time(self, peak_time, peak_attendance, time_graph):
    """
    Adds a peak time and the time graph it came from.
    :param peak_time: an int
    :param time_graph: a list of lists. first list: x values, second list: y values
    """
    self.times.append(peak_time)
    self.peak_attendances.append(peak_attendance)
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

  def get_pairs(self):
    return self.pairs

  def to_dict(self):
    """
    This is the dictionary that gets used by search_controller
    """
    return {
      'times': [{
        'peak': self.times[i], # peak time
        'peak_attendance': self.peak_attendances[i][0],
        'graph': {
          'data': self.time_graphs[i]
        }
      } for i in xrange(0, len(self.times))],
      'venues': [{
        'id': self.venue_ids[i], # id of the venue
        'events': self.venue_events[i] # events that got the venue recommended
      } for i in xrange(0, len(self.venue_ids))],
      'features': self.features,
      'pairs': self.pairs
    }

def top_k_recommendations(events, k=10):

  # Venues

  def venue_avg_weighted_attendance(d, key):
    return sum([e.weighted_attending for e in d[key]])/len(d[key])

  for i in xrange(0, len(events)):
    events[i].weighted_attending = events[i].attending*math.e**(-1*i)

  venues_to_events = defaultdict(list)
  for event in events:
    venues_to_events[event.venue.id].append(event)

  event_lengths = [len(venues_to_events[venue_id]) for venue_id in venues_to_events]
  median_event_length = sorted(event_lengths)[len(event_lengths)/2]

  for venue_id in venues_to_events:
    events = venues_to_events[venue_id]
    for event in events:
      event.weighted_attending *= math.fabs((len(events) - median_event_length) + 0.1)**(-0.5)

  top_venues = sorted(venues_to_events.keys(), key=lambda k: venue_avg_weighted_attendance(venues_to_events, k), reverse=True)
  rec = Recommendation()
  for venue_id in top_venues[:k]:
    rec.add_venue(venue_id, [(event.id, event.name) for event in venues_to_events[venue_id]])

  # Times

  synthetic_time_data = np.asarray([i for i in xrange(0, 24)])
  time_models = topic_regression.topic_time_models(
    preprocessed.events,
    preprocessed.ids_to_topics,
    [e["id"] for e in preprocessed.events].index(events[0].id),
    preprocessed.corpus,
    preprocessed.topic_model
  )
  for time_model in time_models:
    peak_time, peak_attendance = time_model.find_peak(synthetic_time_data)
    model_graph = time_model.generate_graph(synthetic_time_data)
    rec.add_time(peak_time, peak_attendance, model_graph)

  m = MetadataModel(events)
  features_coefs = m.features_coefs()

  # For now, let's return the top three features. We can play around with this or generate a number programmatically

  top_feature_names = filter(lambda feat: features_coefs[feat] > 0,
    sorted(features_coefs.keys(), key=features_coefs.get, reverse=True))
  for feature_name in top_feature_names:
    rec.add_feature(feature_descriptions[feature_name])

  rec.pairs = coupling.suggest_pairs(events, rec.times, rec.venue_ids)

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
    print "Top pairs:"
    print
    for pair in rec.to_dict()["pairs"]:
      print "{} at {}".format(Venue.query.filter_by(id=pair["venue_id"]).first().name, pair["time"])
