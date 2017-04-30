from sklearn.linear_model import LinearRegression

class MetadataModel(object):
  """
  Model for event meta-features.
  The 'coefs' function tells us approximately how important different features are in the model.
  This allows us to say things like "Events like this one are successful when they contain 'food' in the description."
  """
  model = None

  def _contains_links(e):
    """
    Does the event description contain a link?
    """
    return "http://" in e.description.lower()

  def _contains_email(e):
    """
    Does the event description contain an email?
    """
    return "@" in e.description.lower()

  def _contains_food(e):
    """
    Does the event description or title mention food?
    """
    return "food" in e.description.lower().split() or "food" in e.name.lower().split()

  def _contains_free(e):
    """
    Does the event description or title mention the word "free"?
    """
    return "free" in e.description.lower().split() or "free" in e.name.lower().split()

  def __init__(self, events):
    """
    Initializes a linear regression model based on predefined features of a set of events.
    """

    self.description_length = lambda e: len(e.description)
    self.has_profile_picture = lambda e: 1 if e.profile_picture is not None else 0
    self.has_links = lambda e: 1 if self._contains_links(e) else 0
    self.has_category = lambda e: 1 if e.category is not None else 0
    self.has_cover_picture = lambda e: 1 if e.cover_picture is not None else 0
    self.has_email = lambda e: 1 if self._contains_email(e) else 0
    self.has_food = lambda e: 1 if self._contains_food(e) else 0
    self.is_free = lambda e: 1 if self._contains_free(e) else 0

    self.feature_funcs = [
      self.description_length,
      self.has_profile_picture,
      self.has_links,
      self.has_category,
      self.has_cover_picture,
      self.has_email,
      self.has_food,
      self.is_free
    ]

    arr = []
    for event in events:
      feature_values = [func(event) for func in self.feature_funcs]
      arr.append(feature_values)
    feature_mat = np.asarray(arr)
    attendance = np.asarray([event.attendance for event in events])
    self.model = LinearRegression()
    self.model.fit(feature_mat, attendance)
    
  def test(self, event):
    feature_values = [func(event) for func in self.feature_funcs]
    return self.model.predict(feature_values)
    
  def coefs(self):
    return self.model.coef_[0,:]