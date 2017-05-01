import polyfit
import math
import numpy as np

class TimeModel(object):
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
      return [list(i)[0] for i in list(test_values)]
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

    return (np.argmax(test_values), max(test_values))