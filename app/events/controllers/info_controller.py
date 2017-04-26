import json
from . import *
from app.events.models import queries
import Levenshtein

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

namespace = '/info'

@events.route(namespace + '/venues', methods=['GET'])
def get_venues():
  """
  Grab a sample list of venues
  """
  venues = queries.random_venues(10)
  venues = [venue_schema.dump(v).data for v in venues]
  result = {
    'success': True,
    'data': {
      'venues': venues
    }
  }
  return jsonify(result)

@events.route(namespace + '/categories', methods=['GET'])
def get_categories():
  """
  Grab a list of all categories from database events
  """
  categories = app.preprocessed.uniq_categs
  result = {
    'success': True,
    'data': {
      'categories': categories
    }
  }
  return jsonify(result)

@events.route(namespace + '/autocomplete', methods=['GET'])
def autocomplete():
  """
  Recommends words based on a given word using edit distance / startwith
  """
  query = '' if request.args.get('query') is None else request.args.get('query')

  prefixed_words = []
  close_words = []
  for f in app.preprocessed.words:
    lowered = f.lower()
    if lowered.startswith(query) and lowered != query:
      prefixed_words.append(f)
    elif Levenshtein.distance(query, lowered) <= 1:
      close_words.append(f)

  result = {
    'success': True,
    'data': {
      'suggestions': prefixed_words + close_words
    }
  }
  return jsonify(result)
