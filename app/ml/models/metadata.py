import numpy as np
from sklearn.linear_model import LinearRegression

from constants import *
from app.features import *

class MetadataModel(object):
  """
  Model for event meta-features.
  The 'coefs' function tells us approximately how important different features are in the model.
  This allows us to say things like "Events like this one are successful when they contain 'food' in the description."
  """
  model = None

  def __init__(self, events):
    """
    Initializes a linear regression model based on predefined features of a set of events.
    """

    self.features = FEATURES

    indicators = []
    for event in events:
      feature_values = [feature.apply(event) for feature in self.features]
      indicators.append(feature_values)
    feature_mat = np.asarray(indicators)
    attendance = np.asarray([event.attending for event in events])
    self.model = LinearRegression()
    self.model.fit(feature_mat, attendance)

  def features_coefs(self):
    """
    Returns feature names and their importances (coefficients). e.g.

    {"has_food": 0.8,
     "is_free": 13.7,
      ...}
    """
    result = {}
    for i in xrange(0, len(self.features)):
      result[self.features[i].name] = self.model.coef_[i]
    return result
