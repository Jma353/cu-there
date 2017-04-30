from datetime import datetime

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
  return train_data(events, utils.get_hour)