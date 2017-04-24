from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
import numpy as np
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
    self.events        = self._build_events_list()
    self.tfidf_vec     = self._build_tfidf_vec()
    self.doc_by_term   = self._build_doc_by_term(self.events, self.tfidf_vec)
    self.categ_name_to_idx, self.categ_idx_to_name, self.categ_by_term = self._build_categ_by_term(self.events, self.doc_by_term)
    self.words         = self.tfidf_vec.get_feature_names()
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

  def _build_tfidf_vec(self):
    """
    Builds the TfidfVectorizer needed to parse our data-set
    """
    return TfidfVectorizer(
      tokenizer=self.tokenize,
      min_df=5,
      max_df=0.95,
      max_features=5000,
      stop_words='english')

  def _build_doc_by_term(self, events, tfidf_vec):
    """
    Given a list of event dictionaries `events` and a
    TfidfVectorizer `tfidf_vec`, builds a document-by-
    term matrix based on the events' descriptions
    """
    event_descs = [e['description'] for e in events]
    return tfidf_vec.fit_transform(event_descs).toarray()

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

    return categ_name_to_idx, categ_idx_to_name, categ_by_term

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
