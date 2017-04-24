from . import *

# IR / ML
from app.events.models import queries
from app.ir.ir_engine import *
from app.ml.pipeline import *

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
  ir_engine = IREngine(
    query=q,
    categs=[], # TODO: fill with user input
    events=app.preprocessed.events,
    doc_by_term=app.preprocessed.doc_by_term,
    tfidf_vec=app.preprocessed.tfidf_vec,
    categ_by_term=app.preprocessed.categ_by_term,
    categ_name_to_idx=app.preprocessed.categ_name_to_idx
  )

  # Note: just use rocchio function with empty relevant/irrelevant lists
  event_ids = ir_engine.get_rocchio_categ_ranked_results()
  event_ids = event_ids[:min(len(event_ids), 12)] # Take 12 or less
  es = queries.get_events(event_ids)

  # ML, get recs
  recs = top_k_recommendations(es)

  # Endpoint info
  times = [r['time'] for r in recs]
  venues = queries.get_venues([r['venue_id'] for r in recs])

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': [venue_schema.dump(v).data for v in venues],
      'times': times,
      'tags': [],
      'events': [event_schema.dump(e).data for e in es]
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
  relevant   = request.args.getlist('relevant') # ids
  irrelevant = request.args.getlist('irrelevant') # ids

  print 'Relevant IDs:'
  print relevant
  print 'Irrelevant IDs:'
  print irrelevant

  # IR, get events
  ir_engine = IREngine(
    query=q,
    categs=[], # TODO: fill with user input
    events=app.preprocessed.events,
    doc_by_term=app.preprocessed.doc_by_term,
    relevant=relevant,
    irrelevant=irrelevant,
    tfidf_vec=app.preprocessed.tfidf_vec,
    categ_by_term=app.preprocessed.categ_by_term,
    categ_name_to_idx=app.preprocessed.categ_name_to_idx
  )

  event_ids = ir_engine.get_rocchio_categ_ranked_results()
  event_ids = event_ids[:min(len(event_ids), 12)] # Take 12 or less
  es = queries.get_events(event_ids)

  # ML, get recs
  recs = top_k_recommendations(es)

  # Endpoint info
  times = [r['time'] for r in recs]
  venues = queries.get_venues([r['venue_id'] for r in recs])

  print
  print 'Venues found:'
  for v in venues:
    print v.name

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': [venue_schema.dump(v).data for v in venues],
      'times': times,
      'tags': [],
      'events': [event_schema.dump(e).data for e in es]
    }
  }

  return jsonify(response)
