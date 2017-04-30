import numpy as np
from sklearn.linear_model import LinearRegression

from constants import *

class Feature(object):
  def __init__(self, name, func):
    self.name = name
    self.func = func
    
  def apply(self, event):
    return self.func(event)

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

    self.features = [
      Feature(DESCRIPTION_LENGTH, lambda e: len(e.description) if e.description is not None else 0),
      Feature(HAS_PROFILE_PICTURE, lambda e: 1 if e.profile_picture is not None else 0),
      Feature(HAS_LINKS, lambda e: 1 if e.description is not None and "http://" in e.description.lower() else 0),
      Feature(HAS_CATEGORY, lambda e: 1 if e.category is not None else 0),
      Feature(HAS_COVER_PICTURE, lambda e: 1 if e.cover_picture is not None else 0),
      Feature(HAS_EMAIL, lambda e: 1 if e.description is not None and "@" in e.description.lower() else 0),
      Feature(HAS_FOOD, lambda e: 1 if e.description is not None and \
        e.name is not None and "food" in e.description.lower().split() or "food" in e.name.lower().split() else 0),
      Feature(IS_FREE, lambda e: 1 if e.description is not None and \
        e.name is not None and "free" in e.description.lower().split() or "free" in e.name.lower().split() else 0)
    ]

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