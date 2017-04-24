from datetime import datetime

def get_hour(time_string):
  date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
  return date_time.hour + (date_time.minute / 60.0)
  
def get_day(time_string):
  date_time = datetime.strptime(time_string[:-5], '%Y-%m-%dT%H:%M:%S')
  return date_time.day