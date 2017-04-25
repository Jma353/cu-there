import re
import math
import numpy as np
from collections import Counter, defaultdict
from nltk.stem.porter import PorterStemmer

class IREngine(object):
  """
  Input: A text query containing words related to an event
  Output: A ranked list of event_ids based on the most relevant events to query
  """

  def __init__(self, **kwargs):
    query = kwargs.get('query', '')
    categs = kwargs.get('categs', [])
    rel = kwargs.get('rel', [])
    irrel = kwargs.get('irrel', [])
    events = kwargs.get('events', [])
    doc_by_term = kwargs.get('doc_by_term', [])
    count_vec = kwargs.get('count_vec', None)
    categ_by_term = kwargs.get('categ_by_term', [])
    categ_name_to_idx = kwargs.get('categ_name_to_idx', {})

    # Create query vector
    term_to_idx = {v:i for i, v in enumerate(count_vec.get_feature_names())}
    query_vec = np.zeros(len(doc_by_term[0]), dtype = np.float32)

    for term in self.tokenize(query):
      if term in term_to_idx:
        query_vec[term_to_idx[term]] += 1

    self.query = query
    self.categs = categs
    self.rel = rel
    self.irrel = irrel
    self.events = events
    self.n_events = len(self.events)
    self.query_vec = query_vec
    self.doc_by_term = doc_by_term
    self.idx_to_term = {v:k for k,v in term_to_idx.items()}
    self.categ_by_term = categ_by_term
    self.categ_name_to_idx = categ_name_to_idx

  def get_ranked_results(self):
    """
    Return a ranked list of event_ids given query using cosine similarity
    """
    ranked_events = self.get_cos_sim_ranked_events()

    # For testing purposes
    print("Cosine Similarity Results:")
    self.print_top_events(ranked_events, 10)

    if not ranked_events:
        print("No relevant events")

    return [self.events[doc_id]["id"] for _, doc_id in ranked_events]

  def get_rocchio_ranked_results(self):
    """
    Return a ranked list of event_ids given query using cosine
    similarity with Rocchio
    """
    rocchio_ranked_events = self.get_rocchio_rankings(self.rel, self.irrel)

    # For testing purposes
    print("Rocchio Cosine Similarity Results:")
    self.print_top_events(rocchio_ranked_events, 10)

    if not rocchio_ranked_events:
      print("No relevant events")

    return [self.events[doc_id]["id"] for cs, doc_id in rocchio_ranked_events]

  def get_rocchio_categ_ranked_results(self):
    """
    Return a ranked list of event_ids, similar words, and similar categories
    given query using cosine similarity with Rocchio and category incorporated
    """
    rocchio_categ_ranked_events = self.get_rocchio_categ_rankings(self.rel, self.irrel)

    # For testing purposes
    print("Rocchio Category Cosine Similarity Results:")
    self.print_top_events(rocchio_categ_ranked_events, 10)

    if not rocchio_categ_ranked_events:
      print("No relevant events")

    # Get similar terms between query and event
    event_id = ""
    event_sim_words = []
    event_sim_categs = ""
    results = []

    for _, doc_id in rocchio_categ_ranked_events[:10]:
      event_vec = self.doc_by_term[doc_id]
      prod_vec = np.multiply(self.query_vec, event_vec)

      # Get all similar terms between vectors
      prod_list = [(i, p) for i, p in enumerate(prod_vec) if p > 0]
      sim_terms = sorted(prod_list, key=lambda x: -x[1])

      # Get similar category
      sim_categ = self.events[doc_id]['category']  if self.events[doc_id]['category'] in self.categs else ""

      event_id = self.events[doc_id]["id"]
      event_sim_words = [self.idx_to_term[i] for i,_ in sim_terms]
      event_sim_categs = sim_categ
      results.append((event_id, event_sim_words, event_sim_categs))

    return [self.events[doc_id]["id"] for cs, doc_id in rocchio_categ_ranked_events]

  def tokenize(self, text):
    """
    Tokenize text into list of words and stem words
    """
    return re.findall(r'[a-z]+', text.lower()) if text else []

  def stem(self, terms):
    """
    Stem each word in word list using Porter Stemming Algorithm
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(term) for term in terms]

  def build_inverted_index(self, events):
    """
    Build inverted index dictionary
    """
    inv_idx = defaultdict(list)

    for idx, event in enumerate(events):
      # Dict format: {word: # of times word appears in event description}
      term_counts = Counter(self.tokenize(event))

      # Update list of (doc_id, tf) for each word in event
      for term in term_counts:
        inv_idx.setdefault(term, []).append((idx, term_counts[term]))

    return inv_idx

  def compute_idf(self, inv_idx, min_df=5, max_df_ratio=0.95):
    """
    Compute IDFs using inverted index

    min_df: Min number of docs a term must occur in
    max_df_ratio: Max ratio of docs a term can occur in
    """
    idf_dict = {}

    # Ignore too specific and too common terms
    pruned_inv_idx = {k:v for k,v in inv_idx.items()
                    if len(v) >= min_df and
                    ((len(v)/float(self.n_events)) <= max_df_ratio)}

    # Compute IDF for each word in filtered_inv_idx
    for term, doc_tf in pruned_inv_idx.items():
      # TODO: Optimize this so we don't store number of events
      idf = math.log(self.n_events / float(1 + len(doc_tf)), 2)
      idf_dict[term] = idf

    return idf_dict

  def compute_doc_norms(self, inv_idx, idf):
    """
    Compute norm of each event using inverted index
    """
    norms = np.zeros(self.n_events)

    # Compute norm of each event
    for term, doc_tf in inv_idx.items():
      for doc_id, tf in doc_tf:
        norms[doc_id] += pow((tf * idf[term]), 2)

    return np.sqrt(norms)

  def get_cos_sim_list(self, inv_idx, idf, doc_norms):
    """
    Get most similar events using cosine similarity

    Return: list of (score, doc_id)
    """
    # Dict format: {doc_id: unnormalized_score}
    scores = defaultdict(int)

    query_terms = self.tokenize(self.query)
    query_counts = Counter(query_terms)

    # Compute the vectors product
    for term in query_terms:
      # Ignore terms that don't appear in event descriptions
      if term not in inv_idx: continue
      doc_tf_list = inv_idx[term]

      for doc_id, doc_tf in doc_tf_list:
        doc_weight = idf[term] * doc_tf
        query_weight = query_counts[term] * idf[term]
        scores[doc_id] += query_weight * doc_weight

    # Normalize the scores
    for doc_id, score in scores.items():
      doc_norm = float(doc_norms[doc_id])
      idf_tf_sum = 0

      for term, tf in query_counts.items():
        if term not in idf: continue
        idf_tf_sum += math.pow(idf[term]*tf, 2)

      query_norm = math.sqrt(idf_tf_sum)
      scores[doc_id] = float(score) / (doc_norm * query_norm)

    results = sorted(scores.items(), key=lambda x: -x[1])
    results = [(s, d) for d,s in results]

    return results

  def get_cos_sim_ranked_events(self):
    """
    Get ranked list of events based on cosine similarity of event descriptions

    Return: list of event ids
    """
    event_descs = [event["description"] for event in self.events]
    inv_idx = self.build_inverted_index(event_descs)
    idf = self.compute_idf(inv_idx)
    inv_idx = {k:v for k, v in inv_idx.items() if k in idf}
    doc_norms = self.compute_doc_norms(inv_idx, idf)

    return self.get_cos_sim_list(inv_idx, idf, doc_norms)

  def print_top_events(self, ranked_events, top_k):
    """
    Print out top_k ranked list of events
    """
    print("#" * len(self.query))
    print(self.query)
    print("#" * len(self.query))

    for score, doc_id in ranked_events[:top_k]:
      print("[{:.2f}] {}: {}".format(
            score,
            self.events[doc_id]['name'].encode('utf-8'),
            self.events[doc_id]['category'].encode('utf-8')))
    print

  def get_cos_sim(self, vec1, vec2):
    """
    Get cosine similarity between two vectors
    """
    vec_prod = np.dot(vec1, vec2)
    vec_norm_prod = np.linalg.norm(vec1) * np.linalg.norm(vec2)

    return vec_prod / float(vec_norm_prod) if vec_norm_prod != 0 else 0

  def run_rocchio(self, rel, irrel, a=1, b=0.8, c=1, clip=True):
    """
    Run Rocchio algorithm to get new query vector
    """
    query_part, rel_part, irrel_part = 0, 0, 0

    # Calculate query_part
    query_part = a * self.query_vec

    # Calculate rel_part
    if rel:
      rel_vecs = [self.doc_by_term[r] for r in rel]
      rel_vecs = np.sum(rel_vecs, axis=0)
      rel_part = b * (rel_vecs / float(len(rel)))

    # Calculate irrel_part
    if irrel:
      irrel_vecs = [self.doc_by_term[r] for r in irrel]
      irrel_vecs = np.sum(irrel_vecs, axis=0)
      irrel_part = c * (irrel_vecs / float(len(irrel)))

    # Calculate new query vector
    new_query_vec = query_part + rel_part - irrel_part

    # Clip negative values to 0 if clip = True
    return np.array([t if t >= 0 else 0 for t in new_query_vec]) if clip else new_query_vec

  def get_rocchio_rankings(self, rel, irrel):
    """
    Get new ranked event list using new Rocchio query vector
    """
    # Get new query vector using Rocchio
    q_vec = self.run_rocchio(rel, irrel)

    # Get cosine similarity of Rocchio vector and each event vector
    cos_sims = [self.get_cos_sim(q_vec, vec) for vec in self.doc_by_term]

    # Get ranked event list for query
    ranking = [(cos_sims[i], i) for i in np.argsort(cos_sims)[::-1]]

    return ranking

  def get_rocchio_categ_rankings(self, rel, irrel, d=.2):
    """
    Get new ranked event list using new Rocchio query vector and
    taking event categories into account
    """
    # Get new query vector using Rocchio
    q_vec = self.run_rocchio(rel, irrel)

    # Calculate category vector
    idx_categs = [self.categ_name_to_idx[c] for c in self.categs if c in self.categ_name_to_idx]
    categ_vecs = [self.categ_by_term[idx] for idx in idx_categs]

    avg_categ_vec = (np.sum(categ_vecs, axis = 0) / float(len(categ_vecs))) if len(categ_vecs) > 0 else 0

    # Augment new Rocchio vector by average category vector (clip negative values)
    new_vec = q_vec + (d * avg_categ_vec)

    # Get ranked event list based on cosine similarity
    cos_sims = [self.get_cos_sim(new_vec, vec) for vec in self.doc_by_term]
    ranking = [(cos_sims[i], i) for i in np.argsort(cos_sims)[::-1]]

    return ranking
