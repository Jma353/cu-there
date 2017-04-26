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
  c) `w` occurs within the same document as `v_i` (coocurrence)

  a) and b) are scored based on PMI, c) by sheer # of similar documents

  A word `w_i's relationship with another word `w_j` can be determined
  by scoring all these features for `w_i` and `w_j`, determining the
  cosine-similarity between each respective feature for `w_i` and `w_j`
  (compare `w_i`'s a and `w_j`'s a, their b's, etc.) and then weighting
  the two words' similarity with the following equation:

  A*a_sim + B*b_sim + C*c_sim

  A, B, and C are all parameters of this object
  """

  def __init__(self, A, B, C, preprocessed):
    """
    Constructor
    """
    assert C == 1.0 # Must be true
    self.A = A
    self.B = B
    self.C = C
    self.p = preprocessed

  def related_words(self, word, k=10):
    """
    Up to k related words for word `word` based on training data
    """
    # Grab pointers
    words       = self.p.words
    word_to_idx = self.p.word_to_idx

    # Handle this accordingly
    if word not in word_to_idx: return []

    # Grab vectors
    # five_after  = self.p.five_words_after[word_to_idx[word]]
    # five_before = self.p.five_words_before[word_to_idx[word]]
    coocurr     = self.p.coocurrence[word_to_idx[word]]

    # Result vectors
    # alpha = self.batch_cosine_sim(five_after, self.p.five_words_after)
    # beta  = self.batch_cosine_sim(five_before, self.p.five_words_before)
    gamma = self.batch_cosine_sim(coocurr, self.p.coocurrence)

    # Linear combination
    result = self.C * gamma # self.A * alpha # + self.B * beta + 

    # Grab all words' indexes not corresponding to `word`'s index
    ranking = [r for r in result.argsort()[::-1] if r != word_to_idx[word]]

    # Get top k words
    return [words[i] for i in ranking[:k]]

  def batch_cosine_sim(self, vector, matrix):
    """
    Cosine similarity in numpy, batched form
    """
    # Dot product
    dot_prod = np.dot(vector, matrix.T)
    # Norms
    vec_norm = np.linalg.norm(vector)
    mat_norm = np.linalg.norm(matrix, axis=1)
    # Denominator
    denom = mat_norm * vec_norm
    denom[denom == 0.0] = 1
    return dot_prod / denom

  def add_sim_words(self, query, k):
    """
    Adds the top k similar words to the query `query` and
    returns a new query in string form
    """
    q_sp = re.split(r'\s+',query)
    other_werds = []
    for w in q_sp:
      other_werds.extend(self.related_words(w)[:k])
    other_werds = list(set(other_werds)) # Remove duplicates
    print 'Found new words to add to your query!'
    for o in other_werds:
      print o
    return ' '.join(q_sp + other_werds)
