import sys
import json
import re
import math
import numpy as np
from collections import Counter
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

### Global variables ###
events_dict = {}
events = []
doc_by_term = []
term_to_idx = {}

def main():
  global doc_by_term, events, events_dict, term_to_idx

  # Get command-line arguments
  args = sys.argv

  if len(args) < 2:
    print("Please provide event description.")
    quit()

  # First argument is event description
  event_desc = args[1]

  # Load events from events json file
  with open("events.json") as events_json:
    events_dict = json.load(events_json)

  # Only store useful information from events dictionary
  events = [{"id": event["id"], "name": event["name"],
            "description": event["description"] if event["description"] else "",
            "category": event["category"] if event["category"] else ""}
            for event in events_dict]

  event_descs = [event["description"] for event in events]

  # Print top events based on cosine similarity
  ranked_events = get_cos_sim_ranked_events(event_desc, event_descs)
  print_top_events(event_desc, ranked_events, events_dict, 10)
  ranked_events = [doc_id for _, doc_id in ranked_events]

  # Make doc-term matrix
  tfidf_vec = TfidfVectorizer(min_df=5,
                              max_df=0.95,
                              max_features=3000,
                              stop_words='english')

  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()
  term_to_idx = {v:i for i, v in enumerate(tfidf_vec.get_feature_names())}

  get_rocchio_rankings(event_desc, ranked_events, [])

### Helper Functions ###

def tokenize(text):
  """
  Tokenize text into list of words and stem words
  """
  return re.findall(r'[a-z]+', text.lower()) if text else []

def stem(words):
  """
  Stem each word in word list using Porter Stemming Algorithm
  """
  stemmer = PorterStemmer()
  return [stemmer.stem(word) for word in words]

def build_inverted_index(events):
  """
  Build inverted index dictionary
  """
  inv_idx = defaultdict(list)

  for idx, event in enumerate(events):
    # Dict format: {word: # of times word appears in event description}
    word_counts = Counter(tokenize(event))

    # Update list of (doc_id, tf) for each word in event
    for word in word_counts:
      inv_idx.setdefault(word, []).append((idx, word_counts[word]))

  return inv_idx

def compute_idf(inv_idx, n_events, min_df=5, max_df_ratio=0.95):
  """
  Compute IDFs using inverted index

  min_df: Min number of docs a term must occur in
  max_df_ratio: Max ratio of docs a term can occur in
  """
  idf_dict = {}

  # Ignore too specific and too common words
  pruned_inv_idx = {k:v for k,v in inv_idx.items()
                    if len(v) >= min_df and
                    ((len(v)/float(n_events)) <= max_df_ratio)}

  # Compute IDF for each word in filtered_inv_idx
  for word, doc_tf in pruned_inv_idx.items():
    # TODO: Optimize this so we don't store number of events
    idf = math.log(n_events / float(1 + len(doc_tf)), 2)
    idf_dict[word] = idf

  return idf_dict

def compute_doc_norms(inv_idx, idf, n_events):
  """
  Compute norm of each event using inverted index
  """
  norms = np.zeros(n_events)

  # Compute norm of each event
  for word, doc_tf in inv_idx.items():
    for doc_id, tf in doc_tf:
      norms[doc_id] += pow((tf * idf[word]), 2)

  return np.sqrt(norms)

def get_cos_sim_list(query, inv_idx, idf, doc_norms):
  """
  Get most similar events using cosine similarity

  Return: list of (score, doc_id)
  """
  # Dict format: {doc_id: unnormalized_score}
  scores = defaultdict(int)

  query_words = tokenize(query)
  query_counts = Counter(query_words)

  # Compute the vectors product
  for word in query_words:
    # Ignore words that don't appear in event descriptions
    if word not in inv_idx: continue
    doc_tf_list = inv_idx[word]
    for doc_id, doc_tf in doc_tf_list:
      doc_weight = idf[word] * doc_tf
      query_weight = query_counts[word] * idf[word]
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

def get_cos_sim_ranked_events(query, event_descs):
  """
  Get ranked list of events based on cosine similarity of event descriptions

  Return: list of event ids
  """
  inv_idx = build_inverted_index(event_descs)
  idf = compute_idf(inv_idx, len(event_descs))
  inv_idx = {k:v for k, v in inv_idx.items() if k in idf}
  doc_norms = compute_doc_norms(inv_idx, idf, len(event_descs))

  return get_cos_sim_list(query, inv_idx, idf, doc_norms)

def print_top_events(query, ranked_events, events_dict, top_k):
  """
  Print out top_k ranked list of events
  """
  print("#" * len(query))
  print(query)
  print("#" * len(query))

  for score, doc_id in ranked_events[:top_k]:
    category = "N/A"

    if events_dict[doc_id]['category']:
      category = events_dict[doc_id]['category']

    print("[{:.2f}] {}: {}".format(
          score,
          events_dict[doc_id]['name'].encode('utf-8'),
          category.encode('utf-8')))

def get_categ_sim(events, categs):
  """
  Get category cosine similarity matrix
  """
  # Dict format: {category: [events marked as category]}
  categ_to_event = defaultdict(list)

  for idx, categ in enumerate(categs):
    categ_to_event.setdefault(categ,[]).append(idx)

  uniq_categs = [c for c in categ_to_event.keys()]
  categ_name_to_idx = {name:idx for idx, name in enumerate(uniq_categs)}
  categ_idx_to_name = {v:k for k,v in categ_name_to_idx.items()}
  categ_by_term = np.empty([len(uniq_categs), doc_by_term.shape[1]])

  # Build category_by_words matrix
  for idx, _ in enumerate(categ_by_term):
    # Get event vectors for category
    categ = categ_idx_to_name[idx]
    event_vecs = [doc_by_term[event] for event in categ_to_event[categ]]

    # Calculate category average vector
    vec_sum = np.sum(event_vecs, axis=0)
    norm = np.linalg.norm(vec_sum)
    avg_tfidf_vec = vec_sum / float(norm)
    categ_by_term[idx,:] = avg_tfidf_vec

  return np.dot(categ_by_term, categ_by_term.T)

def get_cos_sim(vec1, vec2):
  """
  Get cosine similarity between two vectors
  """
  vec_prod = np.dot(vec1, vec2)
  vec_norm_prod = np.linalg.norm(vec1) * np.linalg.norm(vec2)

  return vec_prod / float(vec_norm_prod) if vec_norm_prod != 0 else 0

def run_rocchio(query, rel, irrel, a=1, b=0.8, c=1, clip=True):
  """
  Run Rocchio algorithm to get new query vector
  """
  global doc_by_term, term_to_idx

  query_part, rel_part, irrel_part = 0, 0, 0

  # Calculate query_part
  query_vec = np.zeros(len(doc_by_term[0]), dtype = np.float32)

  for term in tokenize(query):
    if term in term_to_idx:
      query_vec[term_to_idx[term]] += 1

  query_part = a * query_vec

  # Calculate rel_part
  if rel:
    rel_mov_vecs = [doc_by_term[r] for r in rel]
    rel_mov_vecs = np.sum(rel_mov_vecs, axis=0)
    rel_part = b * (rel_mov_vecs / float(len(rel)))

  # Calculate irrel_part
  if irrel:
    irrel_mov_vecs = [doc_by_term[r] for r in irrel]
    irrel_mov_vecs = np.sum(irrel_mov_vecs, axis=0)
    irrel_part = c * (irrel_mov_vecs / float(len(irrel)))

  # Calculate new query vector
  new_query_vec = query_part + rel_part - irrel_part

  # Clip negative values to 0 if clip = True
  return np.array([t if t >= 0 else 0 for t in new_query_vec]) if clip else new_query_vec

def get_rocchio_rankings(query, rel, irrel):
  """
  Get new ranked event list using new Rocchio query vector
  """
  global doc_by_term, events, events_dict

  # Get new query vector using Rocchio
  q_vec = run_rocchio(query, rel, irrel)

  # Get cosine similarity of Rocchio vector and each event vector
  cos_sims = [get_cos_sim(q_vec, vec) for vec in doc_by_term]

  # Get ranked movie list for query
  ranking = [(cos_sims[i], i) for i in np.argsort(cos_sims)[::-1]]

  return ranking

if __name__ == '__main__':
    main()
