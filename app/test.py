import sys
import json
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from ir_engine import IREngine

def print_top_sim_words(matrix, idx_to_term, top_k=50):
  """
  Print top_k most and least similar word pairs given coocurrence matrix
  """
  # List format: [("c1 c2", cos_sim)...]
  sims = []

  # Build categ_sims list
  for i in range(len(matrix)):
    for j in range(i+1, len(matrix)):
      c1, c2 = idx_to_term[i], idx_to_term[j]
      cos_sim = matrix[i][j]

      sims.append((c1 + " " + c2, cos_sim))

  # Sort sims list by cosine similarity
  score_list = sorted(sims, key=lambda x: -x[1])

  # Print top k most similar pairs of words
  print("MOST SIMILAR:")
  for (words, score) in score_list[:top_k]:
    print("[%.2f] %s" % (score, words))

  print

  # Print top k most dissimilar pairs of words
  print("LEAST SIMILAR:")
  for (words, score) in score_list[-top_k:][::-1]:
    print("[%.2f] %s" % (score, words))

def init_ir_engine():
  """
  Initialize IREngine with the query and data structures
  """
  ### Get command-line arguments ###

  args = sys.argv

  if len(args) < 3:
    print("Please provide event description and categories.")
    quit()

  query, query_categs = args[1], args[2].split(",")

  events = []

  with open("../events.json") as events_json:
    events_dict = json.load(events_json)

    # List of event dicts containing id, name, description, category
    events = [{"id": event["id"], "name": event["name"],
              "description": event["description"] if event["description"] else "N/A",
              "category": event["category"] if event["category"] else "N/A"}
              for event in events_dict]

  ### Create doc-term matrix ###

  tfidf_vec = TfidfVectorizer(min_df=5, max_df=0.95, max_features=5000, stop_words='english')
  event_descs = [event["description"] for event in events]
  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()

  tfidf_vec = TfidfVectorizer(min_df=5, max_df=0.95, max_features=5000, stop_words='english')
  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()

  ### Create co-occurence matrix ###

  bin_doc_by_term = doc_by_term.copy()
  bin_doc_by_term[bin_doc_by_term > 0] = 1
  cooccurence_matrix = np.dot(bin_doc_by_term.T, bin_doc_by_term)
  np.fill_diagonal(cooccurence_matrix, 0)

  # Testing: print out most and least similar word pairs
  # term_to_idx = {v:i for i, v in enumerate(tfidf_vec.get_feature_names())}
  # idx_to_term = {v:k for k, v in term_to_idx.items()}
  # print_top_sim_words(cooccurence_matrix, idx_to_term)

  ### Create category-term matrix ###

  categs = [event["category"] for event in events]

  # Dict format: {category: [events marked as category]}
  categ_to_event = defaultdict(list)

  for idx, categ in enumerate(categs):
    if categ != "N/A":
      categ_to_event.setdefault(categ,[]).append(idx)

  uniq_categs = [c for c in categ_to_event.keys()]
  categ_name_to_idx = {name:idx for idx, name in enumerate(uniq_categs)}
  categ_idx_to_name = {v:k for k,v in categ_name_to_idx.items()}
  categ_by_term = np.empty([len(uniq_categs), len(doc_by_term[0])])

  # Build categ_by_term matrix
  for idx, _ in enumerate(categ_by_term):
    # Get event vectors for category
    categ = categ_idx_to_name[idx]
    event_vecs = [doc_by_term[event] for event in categ_to_event[categ]]

    # Calculate category average vector
    vec_sum = np.sum(event_vecs, axis=0)
    norm = np.linalg.norm(vec_sum)
    avg_tfidf_vec = vec_sum / float(norm)
    categ_by_term[idx,:] = avg_tfidf_vec

  ### Create IR Engine ###

  ir_engine = IREngine(query=query, events=events, categs=query_categs, doc_by_term=doc_by_term, tfidf_vec=tfidf_vec, categ_by_term=categ_by_term, categ_name_to_idx=categ_name_to_idx)

  return ir_engine

if __name__ == '__main__':
  # Create IR Engine
  ir_engine = init_ir_engine()
  rocchio_ranked_results = ir_engine.get_rocchio_ranked_results()
  rocchio_categ_rankings = ir_engine.get_rocchio_categ_ranked_results()
