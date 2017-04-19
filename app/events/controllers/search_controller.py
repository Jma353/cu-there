from . import *

# IR / ML
from app.events.models import queries
from app.ir_engine import *
from machine_learning.pipeline import *

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

namespace = '/search'

@events.route(namespace, methods=['GET'])
def search():
  """
  Vanilla search (no relevance feedback)
  based on a search query `q`
  """
  # Grab the parameters
  q = '' if request.args.get('q') is None else request.args.get('q')

  # IR, get events
  ir_engine = IREngine(q)
  event_ids = ir_engine.get_ranked_results()
  events = queries.get_events(event_ids)

  # ML, get recs
  recs = top_k_recommendations(events)

  # Endpoint information
  times = [r['time'] for r in recs]
  venues = queries.get_venues([r['venue_id'] for r in recs])

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': [venue_schema.dump(v).data for v in venues],
      'times': times,
      'tags': [],
      'events': [event_schema.dump(e).data for e in events]
    }
  }

  return jsonify(response)

@events.route(namespace + '/rocchio', methods=['GET'])
def search_rocchio():
  """
  Search with Rocchio relevance feedback
  """
  # Grab the parameters
  q          = request.args.get('q')
  relevant   = request.args.get('relevant') # ids
  irrelevant = request.args.get('irrelevant') # ids

  # IR, get events
  # ir_engine = IREngine(q, relevant, irrelevant)
  # event_ids = ir_engine.get_rocchio_rankings()
  # events = queries.get_events(event_ids)
  #
  # ML, get recs
  # times = [r['time'] for r in recs]
  # venues = queries.get_venues([r['venue_id'] for r in recs])
  #
  # Prepare response
  # response = {
  #   'success': True,
  #   'data': {
  #     'venues': [venue_schema.dump(v).data for v in venues],
  #     'times': times,
  #     'tags': [],
  #     'events': [event_schema.dump(e).data for e in events]
  #   }
  # }

  return jsonify({})
