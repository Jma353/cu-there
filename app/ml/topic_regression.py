from gensim import corpora
from models.time import TimeModel
from app.events.models.event import Event
from app import preprocessed
import utils

from collections import defaultdict

def get_index_in_corpus(corpus, doc):
  """
  Gets the .index() of a doc in the corpus
  """
  i = 0
  for document in corpus:
    if document == doc:
      return i
    else:
      i += 1

def topic_time_models(events, events_to_topics, event_index, gensim_corpus, lda_model, k = 20, n_topics=3):
  """
  Takes a query that has been expanded using thesaurus generation,
  a Gensim corpus, a Gensim LDA model, and a parameter k. Finds the topic of the query,
  finds the k documents (events) that are most relevant to this topic, and returns
  a trained TimeModel object.
  """
  # Get doc with event index out of corpus
  
  topic_freqs = defaultdict(int)
  for event in events_to_topics:
    topic_freqs[events_to_topics[event]] += 1
  print topic_freqs
  
  i = 0
  doc_bow = None
  for doc in gensim_corpus:
    if i == event_index:
      doc_bow = doc
    else:
      i += 1
      
  topic_distribution = lda_model[doc_bow]
  
  max = 0
  max_topic = -1
  
  for i in xrange(len(topic_distribution)):
    if topic_distribution[i][1] > max:
      max = topic_distribution[i][1]
      max_topic = topic_distribution[i][0]
      
  max_topics_with_indices = sorted(topic_distribution, key=lambda t: t[1], reverse=True)[:n_topics]
  max_topics = [t[0] for t in max_topics_with_indices]
  
  time_models = []
  
  for max_topic in max_topics:    
    top_event_ids = []
    for event in events:
      event_id = event["id"]
      if events_to_topics[event_id] == max_topic:
        top_event_ids.append(event_id)
      
    top_k = top_event_ids[:k]
    top_k_events = [
      Event.query.filter_by(id=id).first() for id in top_k
    ]
  
    train_data = utils.hour_model_data(top_k_events)
    time_model = TimeModel(feature_func=utils.get_hour)
    time_model.train(train_data, top_k_events)
    time_models.append(time_model)
    
  return time_models