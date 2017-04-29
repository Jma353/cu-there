from scipy.sparse.linalg import svds
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.preprocessing.preprocess import Preprocess

# Preprocessing hand-tests
# TODO - check how many dimensions TFIDF matrix lives in

pp = Preprocess()

def dims_of_closeness(tokenize_method):
  result = pp._build_k_words_near(5, pp.events, pp.term_counts, pp.word_to_idx, tokenize_method)
  u, s, v_trans = svds(result, k=400)
  plt.plot(s[::-1])
  plt.xlabel("Singular value number")
  plt.ylabel("Singular value")
  plt.show()

def dims_of_closeness_before():
  dims_of_closeness(pp.tokenize)

def dims_of_closeness_after():
  dims_of_closeness(pp.rev_tokenize)

dims_of_closeness_after()
