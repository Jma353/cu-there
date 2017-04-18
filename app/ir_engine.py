import sys
import json
import re
import math
import numpy as np
from collections import Counter
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

class IREngine(object):
  """"
  Input: A text query containing words related to an event
  Output: A ranked list of event_ids based on the most relevant events to query
  """

  def __init__(self, query):
    # Load events from events json file
    with open("events.json") as events_json:
      events_dict = json.load(events_json)

      # List of event dicts containing id, name, description, category
      self.events = [{"id": event["id"], "name": event["name"],
                      "description": event["description"] if event["description"] else "",
                      "category": event["category"] if event["category"] else ""}
                       for event in events_dict]
      self.n_events = len(self.events)

    self.query = query
    self.doc_by_term = []
    self.term_to_idx = {}

  def get_ranked_results(self):
    event_descs = [event["description"] for event in self.events]

    # Print top events based on cosine similarity
    ranked_events = self.get_cos_sim_ranked_events()
    self.print_top_events(ranked_events, 10)
    ranked_events = [doc_id for _, doc_id in ranked_events]

    # Make doc-term matrix
    tfidf_vec = TfidfVectorizer(min_df=5,
                                max_df=0.95,
                                max_features=3000,
                                stop_words='english')

    self.doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()
    self.term_to_idx = {v:i for i, v in enumerate(tfidf_vec.get_feature_names())}

    rocchio_ranked_events = self.get_rocchio_rankings(ranked_events, [])
    self.print_top_events(rocchio_ranked_events, 10)

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
    print("#" * len(query))
    print(self.query)
    print("#" * len(query))

    for score, doc_id in ranked_events[:top_k]:
      category = "N/A"

      if self.events[doc_id]['category']:
        category = self.events[doc_id]['category']

      print("[{:.2f}] {}: {}".format(
            score,
            self.events[doc_id]['name'].encode('utf-8'),
            category.encode('utf-8')))

  def get_categ_sim(self):
    """
    Get category cosine similarity matrix
    """
    categs = [event["category"] for event in self.events]

    # Dict format: {category: [events marked as category]}
    categ_to_event = defaultdict(list)

    for idx, categ in enumerate(categs):
      categ_to_event.setdefault(categ,[]).append(idx)

    uniq_categs = [c for c in categ_to_event.keys()]
    categ_name_to_idx = {name:idx for idx, name in enumerate(uniq_categs)}
    categ_idx_to_name = {v:k for k,v in categ_name_to_idx.items()}
    categ_by_term = np.empty([len(uniq_categs), self.doc_by_term.shape[1]])

    # Build category_by_words matrix
    for idx, _ in enumerate(categ_by_term):
      # Get event vectors for category
      categ = categ_idx_to_name[idx]
      event_vecs = [self.doc_by_term[event] for event in categ_to_event[categ]]

      # Calculate category average vector
      vec_sum = np.sum(event_vecs, axis=0)
      norm = np.linalg.norm(vec_sum)
      avg_tfidf_vec = vec_sum / float(norm)
      categ_by_term[idx,:] = avg_tfidf_vec

    return np.dot(categ_by_term, categ_by_term.T)

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
    query_vec = np.zeros(len(self.doc_by_term[0]), dtype = np.float32)

    for term in self.tokenize(self.query):
      if term in self.term_to_idx:
        query_vec[self.term_to_idx[term]] += 1

    query_part = a * query_vec

    # Calculate rel_part
    if rel:
      rel_mov_vecs = [self.doc_by_term[r] for r in rel]
      rel_mov_vecs = np.sum(rel_mov_vecs, axis=0)
      rel_part = b * (rel_mov_vecs / float(len(rel)))

    # Calculate irrel_part
    if irrel:
      irrel_mov_vecs = [self.doc_by_term[r] for r in irrel]
      irrel_mov_vecs = np.sum(irrel_mov_vecs, axis=0)
      irrel_part = c * (irrel_mov_vecs / float(len(irrel)))

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

    # Get ranked movie list for query
    ranking = [(cos_sims[i], i) for i in np.argsort(cos_sims)[::-1]]

    return ranking

if __name__ == '__main__':
  # Get command-line arguments
  args = sys.argv

  if len(args) < 2:
    print("Please provide event description.")
    quit()

  query = args[1]

  ir_engine = IREngine(query)
  ir_engine.get_ranked_results()
