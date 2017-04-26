from . import *

# IR / ML
from app.events.models import queries
from app.ir.ir_engine import *
from app.ir.thesaurus import *
from app.ml.pipeline import *

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

# Variables for linear combo
A = 0
B = 0
C = 1.0

# Thesaurus
# thes = Thesaurus(A, B, C, app.preprocessed)

namespace = '/search'

@events.route(namespace, methods=['GET'])
def search():
  """
  Vanilla search (no relevance feedback)
  based on a search query `q`
  """
  # Grab the parameters
  q = '' if request.args.get('q') is None else request.args.get('q')
  categs = [] if request.args.get('categs') is None else request.args.get('categs').split(",")

  # Update query by extending it with similar words
  # q = thes.add_sim_words(q, 3)

  # IR, get events
  ir_engine = IREngine(
    query=q,
    categs=categs,
    events=app.preprocessed.events,
    doc_by_term=app.preprocessed.doc_by_term,
    count_vec=app.preprocessed.count_vec,
    categ_by_term=app.preprocessed.categ_by_term,
    categ_name_to_idx=app.preprocessed.categ_name_to_idx
  )

  # Note: just use rocchio function with empty relevant/irrelevant lists
  events_info = ir_engine.get_rocchio_categ_ranked_results()
  event_ids, sim_words, sim_categs = map(list, zip(*events_info))
  event_ids = event_ids[:min(len(event_ids), 12)] # Take 12 or less
  es = queries.get_events(event_ids)

  # ML, get recs
  recs = top_k_recommendations(es)

  # Endpoint info
  times = [r['time'] for r in recs]
  venues = queries.get_venues([r['venue_id'] for r in recs])

  # Serialize events + add IR info
  events = [event_schema.dump(e).data for e in es]
  for i in xrange(0, len(events)):
    events[i]['sim_words'] = sim_words[i]
    events[i]['sim_categs'] = sim_categs[i]

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': [venue_schema.dump(v).data for v in venues],
      'times': times,
      'tags': [],
      'events': events
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
  categs = [] if request.args.get('categs') is None else request.args.get('categs').split(",")

  # Update query by extending it with similar words
  q = thes.add_sim_words(q, 5)
  print 'Relevant IDs:'
  print relevant
  print 'Irrelevant IDs:'
  print irrelevant

  # IR, get events
  ir_engine = IREngine(
    query=q,
    categs=categs,
    events=app.preprocessed.events,
    doc_by_term=app.preprocessed.doc_by_term,
    relevant=relevant,
    irrelevant=irrelevant,
    count_vec=app.preprocessed.count_vec,
    categ_by_term=app.preprocessed.categ_by_term,
    categ_name_to_idx=app.preprocessed.categ_name_to_idx
  )

  events_info = ir_engine.get_rocchio_categ_ranked_results()
  event_ids, sim_words, sim_categs = map(list, zip(*events_info))
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

  # Serialize events + add IR info
  events = [event_schema.dump(e).data for e in es]
  for i in xrange(0, len(events)):
    events[i]['sim_words'] = sim_words[i]
    events[i]['sim_categs'] = sim_categs[i]

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': [venue_schema.dump(v).data for v in venues],
      'times': times,
      'tags': [],
      'events': events
    }
  }

  return jsonify(response)
