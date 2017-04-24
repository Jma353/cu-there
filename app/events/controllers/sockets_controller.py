from . import *
import Levenshtein

# Grab socketio instance
socketio = app.socketio

@socketio.on('connect', namespace='/search')
def ws_conn():
  """
  Search socket connection sanity check
  """
  socketio.emit('connect', 'Someone is searching..', '/search')

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
  session = q['session']
  query = q['query']

  words = []
  for f in app.features:
    if Levenshtein.distance(query, f) <= 2:
      words.append(f)

  socketio.emit(session, words, namespace='/search')
