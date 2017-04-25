import numpy as np

DEGREE = 2

def add_anchors(train_set):
  """ Adds 'anchor' points of value 0 at the min and max values
      in the dataset to add concave-downness to the dataset. """
  min_x = min(train_set[:,0])
  max_x = max(train_set[:,0])
  new_train_set = np.asarray([np.asarray(item) for item in zip(
    np.append(
      np.append(
        [min_x - 1],
        train_set[:,0]
      ), [max_x + 1]), 
    np.append(
      np.append([0],
        train_set[:,1]
      ), [0])
  )])
  return new_train_set
  
def add_bump(train_set):
  """ Adds 'bump' of slightly elevated value at the median value
      in the dataset to add concave-downness to the dataset. """
  median_x = train_set[len(train_set[:,0])/2, 0]
  median_y = train_set[len(train_set[:,0])/2, 1]
  new_train_set = np.asarray([np.asarray(item) for item in zip(
    np.append(train_set[:,0],
      [median_x]),
    np.append(train_set[:,1],
      [(median_y * 1.5) + 1])
  )])
  return new_train_set
  
def generate_weights(train_set):
  """ Generates weights for the polyfit. Computes a 'concavity contribution
      score' for each pair of points and weights points proportionally to the
      average of the concavity contribution score of the two pairs it is a part of."""
  
  def _concavity_contribution_score(x1, y1, x2, y2, sum_y, med_x):
    """ Normalized score crudely indicating how 'concave down' a pair of points is.
        If the points are before the median, we check how positive delta y is.
        If the points are after the median, we check how negative delta y is. """
    if x1 < med_x:
      return max((y2-y1)/(sum_y*1.0), 0)
    else:
      return max((y1-y2)/(sum_y*1.0), 0)

  w = []
  
  sum_y = sum(train_set[:,1])
  med_x = train_set[len(train_set[:,0])/2, 0]
  
  # Generating weights based on concavity contribution score
  
  # Edge case for i = 0
  
  ccs_0 = _concavity_contribution_score(
    x1=train_set[0,0],
    x2=train_set[1,0],
    y1=train_set[0,1],
    y2=train_set[1,1],
    sum_y=sum_y,
    med_x=med_x
  )
  w.append(ccs_0)
  
  # Middle section of the dataset

  for i in xrange(1, len(train_set)-1):
    ccs_left = _concavity_contribution_score(
      x1=train_set[i-1,0],
      x2=train_set[i,0],
      y1=train_set[i-1,1],
      y2=train_set[i,1],
      sum_y=sum_y,
      med_x=med_x
    )
    ccs_right = _concavity_contribution_score(
      x1=train_set[i,0],
      x2=train_set[i+1,0],
      y1=train_set[i,1],
      y2=train_set[i+1,1],
      sum_y=sum_y,
      med_x=med_x
    )
    w.append((ccs_left+ccs_right)/2)
    
  # Last data point
  
  ccs_last = _concavity_contribution_score(
    x1=train_set[len(train_set)-2,0],
    x2=train_set[len(train_set)-1,0],
    y1=train_set[len(train_set)-2,1],
    y2=train_set[len(train_set)-1,1],
    sum_y=sum_y,
    med_x=med_x
  )
  w.append(ccs_last)
  
  return w

def create_fit(train_set):
  """ Returns a numpy polyfit (polynomial) object. """
  adjusted_train_set = add_bump(add_anchors(train_set))
  weights = generate_weights(adjusted_train_set)
  return np.poly1d(np.polyfit(adjusted_train_set[:,0], adjusted_train_set[:,1], DEGREE, w=weights))
  
#train = np.asarray([[1,2], [2,3], [3,4]])
#print add_anchors(train)
#print add_bump(train)
#print generate_weights(train)