from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
from Queue import Queue # Thread-safe, job queue
import collections
import numpy as np
import threading
import os
import json
import re

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
    self.doc_by_term_count = self._build_doc_by_term_count(self.events, self.count_vec).toarray()
    self.doc_by_term       = self._build_doc_by_term(self.doc_by_term_count)
    self.words             = self.count_vec.get_feature_names()
    self.word_to_idx       = self._build_word_to_idx_dict(self.words)
    self.coocurrence       = self._build_cooccurence(self.doc_by_term)
    self.five_words_before = self._build_k_words_before(5, self.events, self.doc_by_term_count, self.word_to_idx)
    self.five_words_after  = self._build_k_words_after(5, self.events, self.doc_by_term_count, self.word_to_idx)
    self.uniq_categs, self.categ_name_to_idx, self.categ_idx_to_name, self.categ_by_term = self._build_categ_by_term(self.events, self.doc_by_term)
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
      max_features=5000,
      stop_words='english')

  def _build_doc_by_term_count(self, events, count_vec):
    """
    Given a list of event dictionaries `events` and a
    CountVectorizer `count_vec`, builds a term frequency
    document-by-term matrix based on the events' descriptions
    """
    event_descs = [e['description'] for e in events]
    return count_vec.fit_transform(event_descs)

  def _build_doc_by_term(self, count_matrix):
    """
    Given a list of event dictionaries `events` and a
    term-frequency matrix `count_matrix`, builds a document-by-
    term matrix based on the events' descriptions
    """
    tfidf_transformer = TfidfTransformer()
    return tfidf_transformer.fit_transform(count_matrix).toarray()

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
    uniq_categs = [c for c in categ_to_event.keys()]
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

  def _build_k_words_near(self, k, events, doc_by_term_count, word_to_idx, tokenize, num_threads):
    """
    Given a `k`, a list of event dictionaries `events`,
    a word-to-index mapping `word_to_idx`, and a
    term-document matrix `doc_by_term_count` (freq count),
    build a matrix mapping words to the frequencies at
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
    result = np.empty((num_words, num_words))

    # Lock / function needed for atomic numpy increments
    lock = threading.Lock()
    def incr_result(i, j):
      lock.acquire()
      result[i][j] += 1
      lock.release()

    # Queue of jobs we're gonna be pulling from
    e_q = Queue()

    # Describes work procedure of a thread handling this
    # counting operation
    def worker():
      while True:
        event = e_q.get()
        tokens = tokenize(event['description'])
        q = collections.deque()
        for w in tokens:
          for w_1 in list(q):
            if w in word_to_idx and w_1 in word_to_idx:
              incr_result(word_to_idx[w], word_to_idx[w_1])
          if len(q) == k: q.pop() # Pop from right if we currently have k
          q.appendleft(w) # Append to left a new word w
        e_q.task_done()

    # Spawn those threads
    for i in xrange(num_threads):
      t = threading.Thread(target=worker)
      t.daemon = True
      t.start()

    # Add event "jobs" to the queue
    for e in events:
      e_q.put(e)

    # Wait for everything to finish
    e_q.join()

    # Convert PMI

    # Sigma resultants
    count_f = float(np.sum(result))
    count_w = float(np.sum(doc_by_term_count))

    # Row-wise probabilities for words + features -> dot-product
    p_w     = (np.sum(doc_by_term_count, axis=0) / count_w)
    p_f     = (np.sum(result, axis=0) / count_f)

    # Reshape (1D -> 2D)
    p_w = np.reshape(p_w, (-1, p_w.shape[0])).T
    p_f = np.reshape(p_f, (-1, p_f.shape[0]))

    # Find our answer
    divisor = np.dot(p_w, p_f)
    divisor[divisor == 0.0] = 1.0
    about_to_log = np.divide(result / count_w, divisor)
    about_to_log[about_to_log == 0.0] = 1.0
    result = np.log2(about_to_log)

    return result

  def _build_k_words_before(self, k, events, doc_by_term_count, word_to_idx, num_threads=30):
    """
    Given a `k`, a list of event dictionaries `events`,
    a word-to-index mapping `word_to_idx`, and a
    term-document matrix `doc_by_term`,
    build a matrix mapping words to the frequencies at
    which other words in the data-set appeared within k
    words before that particular word...

    Uses the `tokenize` function to determine how to tokenize
    the description of each event.

    Uses `num_threads` threads to increase the speed at which
    this preprocessing procedure occurs.
    """
    return self._build_k_words_near(k, events, doc_by_term_count, word_to_idx, self.tokenize, num_threads)

  def _build_k_words_after(self, k, events, doc_by_term_count, word_to_idx, num_threads=30):
    """
    Given a `k`, a list of event dictionaries `events`,
    a word-to-index mapping `word_to_idx`, and a
    term-document matrix `doc_by_term`,
    build a matrix mapping words to the frequencies at
    which other words in the data-set appeared within k
    words after that particular word...

    Uses the `tokenize` function to determine how to tokenize
    the description of each event.

    Uses `num_threads` threads to increase the speed at which
    this preprocessing procedure occurs.
    """
    return self._build_k_words_near(k, events, doc_by_term_count, word_to_idx, self.rev_tokenize, num_threads)

  def _build_cooccurence(self, doc_by_term):
    """
    Given a term-document-matrix `doc_by_term`,
    develop a co-occurence matrix
    """
    bin_doc_by_term = doc_by_term.copy()
    bin_doc_by_term[bin_doc_by_term > 0] = 1
    return np.dot(bin_doc_by_term.T, bin_doc_by_term)

  def stem(self, terms):
    """
    Stem each word in word list using Porter Stemming Algorithm
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(term) for term in terms]

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
