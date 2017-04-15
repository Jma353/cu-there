# Data processing tools
# This file contains JsonLoader: an object that yields data for various ML models using data from a JSON file

from datetime import datetime
import json
import numpy as np

class JsonLoader(object):
    """ Class for loading consolidated event data
    (JSON array) into a format easily usable by the models in predictive_models.py """

    _events = []

    def __init__(self):
        self._events = []

    def __init__(self, filename):
        self.load_data(filename)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            self._events = json.loads(f.read())

    def time_model_data(self):
        """ Returns a training set for TimeModel. """

        def _get_hour(time_string):
            date_time = datetime.strptime(time_string[:-5], "%Y-%m-%dT%H:%M:%S")
            return date_time.hour + (date_time.minute / 60.0)

        attendance = [event["stats"]["attending"] for event in self._events]
        time = [_get_hour(event["start_time"]) for event in self._events]
        attendance_time = zip(time, attendance)
        return np.asarray(attendance_time)

#j = JsonLoader("../results/1491923869-consolidation.json")
#print j.time_model_data()
