import json
from . import *
from app.events.models import queries

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

# From here: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
def levenshtein(s1, s2):
  if len(s1) < len(s2):
    return levenshtein(s2, s1)

  # len(s1) >= len(s2)
  if len(s2) == 0:
    return len(s1)

  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      # j+1 instead of j since previous_row and current_row are one character longer
      insertions = previous_row[j + 1] + 1
      deletions = current_row[j] + 1 # than s2
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row

  return previous_row[-1]

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
    elif levenshtein(query, lowered) <= 1:
      close_words.append(f)

  result = {
    'success': True,
    'data': {
      'suggestions': prefixed_words + close_words
    }
  }
  return jsonify(result)
