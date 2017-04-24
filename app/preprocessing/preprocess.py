from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
import numpy as np
import os
import json
import re

class Preprocess(object):
  """
  Object driving access to all required preprocessed data-structures,
  matricies, and indexes needed for IR tasks like TFIDF, thesaurus-
  building, etc.
  """

  def __init__(self):
    pass


  # TODO
