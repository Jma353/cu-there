from datetime import datetime
from collections import defaultdict
import numpy as np

def get_hour(time_string):
  date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
  return date_time.hour + (date_time.minute / 60.0)
  
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
  return train_data(events, get_hour)
  
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