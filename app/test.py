import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from ir_engine import IREngine

if __name__ == '__main__':
  # Get command-line arguments
  args = sys.argv

  if len(args) < 2:
    print("Please provide event description.")
    quit()

  query = args[1]

  # Testing
  events = {}

  with open("../events.json") as events_json:
    events_dict = json.load(events_json)

    # List of event dicts containing id, name, description, category
    events = [{"id": event["id"], "name": event["name"],
                    "description": event["description"] if event["description"] else "",
                    "category": event["category"] if event["category"] else ""}
                     for event in events_dict]

  # Create doc-term matrix
  tfidf_vec = TfidfVectorizer(min_df=5, max_df=0.95, max_features=5000, stop_words='english')
  event_descs = [event["description"] for event in events]
  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()

  # Create IR Engine
  ir_engine = IREngine(query=query, events=events, doc_by_term=doc_by_term, tfidf_vec=tfidf_vec)
  ranked_results = ir_engine.get_ranked_results()
  rocchio_ranked_results = ir_engine.get_rocchio_ranked_results()
