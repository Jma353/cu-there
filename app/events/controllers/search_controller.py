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
A = 0.5
B = 0.5

# Thesaurus
thes = Thesaurus(A, B, app.preprocessed)

def process_recs(recs):
  # Endpoint info
  venues = queries.get_venues([r['venue_id'] for r in recs])
  venues = [venue_schema.dump(v).data for v in venues] # Resultant
  def _venue_by_id(v_id):
    results = [v for v in venues if v['id'] == v_id]
    return None if len(results) == 0 else results[0]
  for r in recs:
    v = _venue_by_id(r['venue_id'])
    v['events'] = r['events']
    v['suggested_time'] = r['time']

  graphs = []
  for r in recs:
    addition = dict()
    addition['venue_id'] = r['venue_id']
    addition['projected_attendence'] = r['time_graph']
    addition['event_times'] = [
      {
        'event_name': e['name'],
        'time': e['start_time']
      } for e in r['events']]
    graphs.append(addition)

  # Serialize events + add IR info
  events = [event_schema.dump(e).data for e in es]
  for i in xrange(0, len(events)):
    events[i]['sim_words'] = sim_words[i]
    events[i]['sim_categs'] = sim_categs[i]

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': venues,
      'graphs': graphs,
      'tags': [],
      'events': events
    }
  }
  return jsonify(response)

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
  q = thes.add_sim_words(q, 3)

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

  return process_recs(recs)

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
  q = thes.add_sim_words(q, 3)

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

  return process_recs(recs)
