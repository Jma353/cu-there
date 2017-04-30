from sklearn.linear_model import LinearRegression

class TagModel:
  """
  Model for learning based on event tags.
  """
  model = None
  tags = []
  
  def train(self, events):
    """ 
    Builds a feature set based on the tags of the events passed in.
    Creates an indicator variable for each tag and builds a matrix of training data using these variables.
    Trains a linear regression model on this data.
    """
    self.model = None
    self.tags = []
    tag_set = set()
    
    for event in events:
      for tag in event.tags:
        tag_set.add(tag)
        
    self.tags = list(tag_set)
    
    indicators = []
    for event in events:
      event_indicators = []
      for tag in tag_set:
        if tag in event.tags:
          event_indicators.append(1)
        else:
          event_indicators.append(0)
      indicators.append(event_indicators)
    indicator_mat = np.asarray(indicators)
    attendance = np.asarray([e.attending for e in events])
    
    self.model = LinearRegression()
    self.model.fit(indicators, attendance)
    
  def coefs(self):
    """
    Returns tags and their importances (coefficients). e.g.
    
    {'free admission': 3.0,
     'open to public': 0.7,
      ...}
    """
    result = {}
    for i in xrange(0, len(self.tags)):
      result[self.tags[i]] = self.model.coef_[0,i]
    return result