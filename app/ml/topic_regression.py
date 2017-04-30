from gensim import corpora
from models.time import TimeModel
from app.events.models.event import Event
from app import preprocessed
import utils

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

def topic_regression(events, event_index, gensim_corpus, lda_model, k = 20):
  """
  Takes a query that has been expanded using thesaurus generation,
  a Gensim corpus, a Gensim LDA model, and a parameter k. Finds the topic of the query,
  finds the k documents (events) that are most relevant to this topic, and returns
  a trained TimeModel object.
  """
  # Get doc with event index out of corpus
  
  i = 0
  doc_bow = None
  for doc in gensim_corpus:
    if i == event_index:
      doc_bow = doc
    else:
      i += 1
      
  topic_distribution = lda_model[doc_bow]
  print "Topics: {}".format(topic_distribution)
  
  max = 0
  max_topic = -1
  
  for i in xrange(len(topic_distribution)):
    if topic_distribution[i][1] > max:
      max = topic_distribution[i][1]
      max_topic = topic_distribution[i][0]
      
  top_docs = []
  for doc in gensim_corpus:
    topics = lda_model[doc]
    if sorted(topics, key=lambda t: t[1], reverse=True)[0][0] == max_topic:
      top_docs.append(doc)
      
  top_k = top_docs[:k]
  top_k_events = [
    Event.query.filter_by(id=events[get_index_in_corpus(gensim_corpus, doc)]["id"]).first() for doc in top_k
  ]
  
  train_data = utils.hour_model_data(top_k_events)
  time_model = TimeModel(feature_func=utils.get_hour)
  time_model.train(train_data, top_k_events)
  return time_model
  
topic_regression(preprocessed.events, 0, preprocessed.corpus, preprocessed.topic_model)