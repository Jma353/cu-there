from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import defaultdict
from scipy.sparse.linalg import svds
import collections
import numpy as np
import sys
import os
import json
import re
import gc

THREAD_COUNT = 5

class Preprocess(object):
  """
    Object driving construction of and access to all required
  preprocessed data-structures, matricies, and indexes needed
  for IR tasks like TFIDF, thesaurus-building, etc.
  """

  def __init__(self):
    """
    Constructor, where all data-structures are built
    """
    self.events            = self._build_events_list()
    self.count_vec         = self._build_count_vec()
    self.doc_by_term       = self._build_doc_by_term(self._build_doc_by_term_count(self.events, self.count_vec))
    self.words             = self.count_vec.get_feature_names()
    self.word_to_idx       = self._build_word_to_idx_dict(self.words)
    term_counts = self._build_term_counts(self.events, self.count_vec)
    self.five_words_before = self._build_k_words_before(5, self.events, term_counts, self.word_to_idx)
    gc.collect()
    self.five_words_after  = self._build_k_words_after(5, self.events, term_counts, self.word_to_idx)
    gc.collect()
    self.uniq_categs, self.categ_name_to_idx, self.categ_idx_to_name, self.categ_by_term = self._build_categ_by_term(self.events, self.doc_by_term)

    print sys.getsizeof(self.events)
    print sys.getsizeof(self.count_vec)
    print sys.getsizeof(self.doc_by_term)
    print sys.getsizeof(self.words)
    print sys.getsizeof(self.word_to_idx)
    print sys.getsizeof(self.five_words_before)
    print sys.getsizeof(self.five_words_after)
    print sys.getsizeof(self.categ_by_term)

    print 'Preprocessing done....'

  def _build_events_list(self):
    """
    Builds a list of events of the following form:
    [
      {
        'id': *id*,
        'description': *descriptions*,
        'category': *category*
      },
      ...
    ]
    """
    events = []
    with open('events.json') as events_json:
      events.extend(json.load(events_json))
    return [{
      'id': event['id'], 'name': event['name'],
      'description': event['description'] if event['description'] else '',
      'category': event['category'] if event['category'] else ''
    } for event in events]

  def _build_count_vec(self):
    """
    Builds the CountVectorizer needed to parse our data-set
    """
    return CountVectorizer(
      tokenizer=self.tokenize,
      min_df=5,
      max_df=0.95,
      max_features=3000,
      stop_words='english')

  def _build_doc_by_term_count(self, events, count_vec):
    """
    Given a list of event dictionaries `events` and a
    CountVectorizer `count_vec`, builds a term frequency
    document-by-term matrix based on the events' descriptions
    """
    event_descs = [e['description'] for e in events]
    return count_vec.fit_transform(event_descs)

  def _build_term_counts(self, events, count_vec):
    """
    Counts of each term in the data-sets
    """
    return np.sum(self._build_doc_by_term_count(events, count_vec).toarray(), axis=0)

  def _build_doc_by_term(self, count_matrix):
    """
    Given a list of event dictionaries `events` and a
    term-frequency matrix `count_matrix`, builds a document-by-
    term matrix based on the events' descriptions
    """
    tfidf_transformer = TfidfTransformer()
    result = tfidf_transformer.fit_transform(count_matrix).toarray()
    return result

  def _build_categ_by_term(self, events, doc_by_term):
    """
    Given a list of event dictionaries `events` and a
    document-by-term matrix `doc_by_term`, builds a category-
    by-term matrix based on the words that are contained
    in event descriptions matching a particular category

    Returns categ_name_to_idx, categ_idx_to_name, and categ_by_term
    """
    # Get list of categories (repeats are intentional)
    categs = [event['category'] for event in events]
    # Dict format: {category: [events marked as category]}
    categ_to_event = defaultdict(list)
    for idx, categ in enumerate(categs):
      if categ != 'N/A':
        categ_to_event.setdefault(categ,[]).append(idx)

    # Look-up data-structures
    uniq_categs = [c for c in categ_to_event.keys() if c]
    categ_name_to_idx = {name:idx for idx, name in enumerate(uniq_categs)}
    categ_idx_to_name = {v:k for k,v in categ_name_to_idx.items()}

    # Build categ_by_term matrix (NUM_CATEGORIES X NUMBER OF WORDS)
    categ_by_term = np.zeros((len(uniq_categs), len(doc_by_term[0])))
    for i in xrange(len(categ_by_term)):
      # Get event vectors for category
      categ = categ_idx_to_name[i]
      event_vecs =  doc_by_term[categ_to_event[categ], :]

      # Calculate category average vector
      vec_sum = np.sum(event_vecs, axis=0)
      norm = np.linalg.norm(vec_sum)
      avg_tfidf_vec = vec_sum / float(norm)
      categ_by_term[i,:] = avg_tfidf_vec

    return uniq_categs, categ_name_to_idx, categ_idx_to_name, categ_by_term

  def _build_word_to_idx_dict(self, words):
    """
    Given a list of words, map these words to their indices
    """
    return {w:i for i,w in enumerate(words)}

  def _build_k_words_near(self, k, events, term_counts, word_to_idx, tokenize, num_threads):
    """
    Build a matrix mapping words to the frequencies at
    which other words in the data-set appeared within k
    words near the particular word (before or after
    depends on whether the tokenize function doesn't reverse
    the tokens or reverses the tokens respectively)

    Uses the `tokenize` function to determine how to tokenize
    the description of each event.

    Uses `num_threads` threads to increase the speed at which
    this preprocessing procedure occurs.
    """
    # Our goal matrix
    num_words = len(word_to_idx)
    result = np.zeros((num_words, num_words), dtype=np.int8)

    # Increase a partiular cell
    def incr_result(i, j):
      result[i][j] += 1

    # Describes work procedure of handling counting operation
    # counting operation
    def worker(event):
      tokens = tokenize(event['description'])
      q = collections.deque()
      for w in tokens:
        for w_1 in list(q):
          if w in word_to_idx and w_1 in word_to_idx:
            incr_result(word_to_idx[w], word_to_idx[w_1])
        if len(q) == k: q.pop() # Pop from right if we currently have k
        q.appendleft(w) # Append to left a new word w

    for e in events:
      worker(e)

    # Convert PMI

    # Sigma resultants
    count_f = float(np.sum(result))
    count_w = float(np.sum(term_counts))

    # Row-wise probabilities for words + features -> dot-product
    p_w = (term_counts / count_w).T
    p_f = np.sum(result, axis=0) / count_f

    # Reshape (1D -> 2D)
    p_w = np.reshape(p_w, (-1, p_w.shape[0])).T
    p_f = np.reshape(p_f, (-1, p_f.shape[0]))

    # Find our answer
    # divisor is np.dot(p_w, p_f) + remove 0's / negatives
    # Remove 0's from log too
    about_to_log = np.divide(result / count_w, np.where(np.dot(p_w, p_f) == 0.0, 1.0, np.dot(p_w, p_f)))
    result = np.log2(
      np.where(
        np.divide(result / count_w, np.where(
          np.dot(p_w, p_f) == 0.0,
          1.0,
          np.dot(p_w, p_f))
        ) <= 0.0,
        1.0,
        np.divide(result / count_w, np.where(
          np.dot(p_w, p_f) == 0.0,
          1.0,
          np.dot(p_w, p_f))
        )
      )
    )
    result, _, _ = svds(result, k=40)
    return result

  def _build_k_words_before(self, k, events, term_counts, word_to_idx, num_threads=THREAD_COUNT):
    """
    Build a matrix mapping words to the frequencies at
    which other words in the data-set appeared within k
    words before that particular word...

    Uses the `tokenize` function to determine how to tokenize
    the description of each event.

    Uses `num_threads` threads to increase the speed at which
    this preprocessing procedure occurs.
    """
    return self._build_k_words_near(k, events, term_counts, word_to_idx, self.tokenize, num_threads)

  def _build_k_words_after(self, k, events, term_counts, word_to_idx, num_threads=THREAD_COUNT):
    """
    Build a matrix mapping words to the frequencies at
    which other words in the data-set appeared within k
    words after that particular word...

    Uses the `tokenize` function to determine how to tokenize
    the description of each event.

    Uses `num_threads` threads to increase the speed at which
    this preprocessing procedure occurs.
    """
    return self._build_k_words_near(k, events, term_counts, word_to_idx, self.rev_tokenize, num_threads)

  def tokenize(self, text):
    """
    Tokenize text into list of words and stem words (also
    remove links and emails)
    """
    text = text.lower()
    reg = r'(((http|https)\:\/\/(([a-z|0-9]+)\.)*([a-z|0-9]+)\.([a-z|0-9]+)(\/([a-z|0-9]+))*))|([\w\.-]+@[\w\.-]+)'
    emails_links_regex = re.compile(reg)
    text = re.sub(emails_links_regex, '', text)
    return re.findall(r'[a-z]+', text)

  def rev_tokenize(self, text):
    """
    Same as `tokenize` but reverses the order of the tokens
    """
    return self.tokenize(text)[::-1]
