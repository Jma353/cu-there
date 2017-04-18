from . import *
from app.events.models import queries

# IR / ML
from app.ir_engine import *


namespace = '/search'

@events.route(namespace, methods=['GET'])
def search():
  """
  Vanilla search (no relevance feedback)
  based on a search query `q`
  """
  # Grab the query
  q = '' if request.args.get('q') is None else request.args.get('q')
  print queries.get_events(['706304596198314', '398761907162985', '260465731049711', '365609203840212'])
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
