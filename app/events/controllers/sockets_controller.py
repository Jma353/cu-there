from . import *
import Levenshtein
import ast

# Grab socketio instance
socketio = app.socketio

@socketio.on('connect', namespace='/search')
def search_conn():
  print 'Someone is searching'

@socketio.on('disconnect', namespace='/search')
def search_disconn():
  print 'Someone stopped searching'

@socketio.on('search', namespace='/search')
def search(q):
  """
  Expects a socket payload of the following format:
  {
    'session': `client UUID`,
    'query': `query term` (e.g. 'mechanica')
  }
  """
  # Grab session / query from the request
  q = ast.literal_eval(q)
  session = q['session']
  query = q['query'].decode('utf-8')

  words = []
  for f in app.preprocessed.words:
    if Levenshtein.distance(query, f) <= 1:
      words.append(f)

  socketio.emit(session, words, namespace='/search')
