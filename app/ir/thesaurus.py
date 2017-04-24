import re
import math
import numpy as np

class Thesaurus(object):
  """
  Object that generates a thesaurus based on the event / venue
  training data.  Utilizes spatial / document-wise co-occurence
  features, as well as grammatical relationship features to
  rank terms' similarity with each other in the data-set.

  Specifically, the features used are:

  a) `w` occurs within 5 words after `v_i`
  b) `w` occurs within 5 words before `v_i`
  c) `w` occurs within the same document as `v_i`
  d) `w`'s level of grammatical similarity to `v_i`

  These features are scored based on PMI

  A word `w_i's relationship with another word `w_j` can be determined
  by scoring all these features for `w_i` and `w_j`, determining the
  cosine-similarity between each respective feature for `w_i` and `w_j`
  (compare `w_i`'s a and `w_j`'s a, their b's, etc.) and then weighting
  the two words' similarity with the following equation:

  A*a_sim + B*b_sim + C*c_sim + D*d_sim

  A, B, C, and D are all parameters of this object
  """

  def __init__(self, A, B, C, D, preprocessed):
    self.A = A
    self.B = B
    self.C = C
    self.D = D
    self.p = preprocessed
