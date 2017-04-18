from . import *

namespace = '/search'

@events.route(namespace, methods=['GET'])
def search():
  """
  Vanilla search (no relevance feedback)
  based on a search query `q`
  """
  # Grab the query
  q = request.args.get('q')

  # TODO

  return jsonify({})


@events.route(namespace + '/rocchio', methods=['GET'])
def search_rocchio():
  """
  Search with Rocchio relevance feedback
  """
  # Grab the parameters
  q          = request.args.get('q')
  relevant   = request.args.get('relevant') # ids
  irrelevant = request.args.get('irrelevant') # ids 

  # TODO

  return jsonify({})
