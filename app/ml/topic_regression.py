from gensim import corpora
from models.time import TimeModel

def topic_regression(expanded_query, gensim_corpus, lda_model, k = 50):
  """
  Takes a query that has been expanded using thesaurus generation,
  a Gensim corpus, a Gensim LDA model, and a parameter k. Finds the topic of the query,
  finds the k documents (events) that are most relevant to this topic, and
  performs time regression (using TimeModel) using these events as the training set.
  """
  doc_bow = gensim_corpus.dictionary.doc2bow(expanded_query.lower().split())
  topic_distribution = lda_model[doc_bow]
  
  max = 0
  max_topic = -1
  
  for i in xrange(len(topic_distribution)):
    if topic_distribution[i] > max:
      max = topic_distribution[i]
      max_topic = i
      
  # max_topic is the index of the most relevant topic in the distribution
  top_docs_max_topic = sorted(lda_model, key = lambda d: abs(dict(d).get(max_topic, 0)), reverse=True)
  top_k = top_docs_max_topic[:k]
  
  # TODO: get events corresponding to top_k, create a TimeModel with these and get the peaks of the model