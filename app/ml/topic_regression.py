from gensim import corpora
from models.time import TimeModel

def topic_regression(expanded_query, gensim_corpus, lda_model):
  """
  Takes a query that has been expanded using thesaurus generation,
  a Gensim corpus, and a Gensim LDA model. Finds the topic of the query,
  finds all documents (events) that are most relevant to this topic, and
  performs time regression (using TimeModel) using these events as the training set.
  """
  doc_bow = gensim_corpus.dictionary.doc2bow(expanded_query.lower().split())
  topic_distribution = lda_model[doc_bow]
  pass