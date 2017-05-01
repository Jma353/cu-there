from . import *
from dateutil import parser

# IR / ML
from app.events.models import queries
from app.ir.ir_engine import *
from app.ir.thesaurus import *
from app.ml.pipeline import *
from app.features import *
from app.ml.models.constants import *

# MARK - All data-structures

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

# Variables for linear combo
A = 0.5
B = 0.5

# Thesaurus
thes = Thesaurus(A, B, app.preprocessed)

# MARK - Generate IR results

def generate_ir_results(**kwargs):
  q = kwargs.get('q', '')
  categs = kwargs.get('categs', [])
  relevant = kwargs.get('relevant', [])
  irrelevant = kwargs.get('irrelevant', [])

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

  # Everything we need
  return sim_words, sim_categs, es

# MARK - Process ML recommendations

def process_recs(es, sim_words, sim_categs, to_return_related_words, recs):
  # Endpoint info
  venues = queries.get_venues([r['id'] for r in recs['venues']])
  venues = [venue_schema.dump(v).data for v in venues] # Resultant

  def _venue_by_id(v_id):
    results = [v for v in venues if v['id'] == v_id]
    return None if len(results) == 0 else results[0]

  def _event_by_id(e_id):
    results = [e for e in es if e.id == e_id]
    return None if len(results) == 0 else results[0]

  for i in xrange(len(recs['venues'])):
    r = recs['venues'][i]
    v = _venue_by_id(r['id'])
    v['events'] = r['events']

  graphs = []

  for r in recs['times']:
    graphs.append({
      'regression': r['graph']['data'],
      'peak': r['peak'],
      'peak_value': r['peak_attendance']
    })

  # Serialize events + add IR info
  events = [event_schema.dump(e).data for e in es]

  for i in xrange(0, len(events)):
    events[i]['sim_words'] = sim_words[i]
    events[i]['sim_categs'] = sim_categs[i]
    events[i]['features'] = [feature.name for feature in FEATURES if feature.apply(es[i]) == 1]

  new_pairs = []
  for pair in recs['pairs']:
    pair['venue_name'] = queries.get_venues([pair['venue_id']])[0].name
    del pair['venue_id']
    new_pairs.append(pair)

  # Prepare response
  response = {
    'success': True,
    'data': {
      'venues': venues,
      'graphs': graphs,
      'features': recs['features'],
      'events': events,
      'related_words': to_return_related_words,
      'pairs': new_pairs
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
  categs = [] if request.args.get('categs') is None else request.args.get('categs').split(',')
  related_words = [] if request.args.get('related_words') is None else request.args.get('related_words').split(',')

  # Related words
  to_return_related_words = thes.grab_sim_words(q, 3)
  q = q + ' ' + ' '.join(related_words)

  # IR, get events
  sim_words, sim_categs, es = generate_ir_results(
    q=q,
    categs=categs
  )

  # ML, get recs
  recs = top_k_recommendations(es)

  # Formatting, rocess recommendations
  return process_recs(es, sim_words, sim_categs, to_return_related_words, recs.to_dict())


@events.route(namespace + '/rocchio', methods=['GET'])
def search_feedback():
  """
  Search with Rocchio relevance feedback + relevant words
  """
  # Grab the parameters
  q          = request.args.get('q')
  relevant   = request.args.getlist('relevant') # ids
  irrelevant = request.args.getlist('irrelevant') # ids
  categs = [] if request.args.get('categs') is None else request.args.get('categs').split(",")
  related_words = [] if request.args.get('related_words') is None else request.args.get('related_words').split(',')

  # Related words
  to_return_related_words = thes.grab_sim_words(q, 3)
  q = q + ' ' + ' '.join(related_words)

  # IR, get events
  sim_words, sim_categs, es = generate_ir_results(
    q=q,
    categs=categs,
    relevant=relevant,
    irrelevant=irrelevant
  )

  # ML, get recs
  recs = top_k_recommendations(es)

  # Formatting, rocess recommendations
  return process_recs(es, sim_words, sim_categs, to_return_related_words, recs.to_dict())
