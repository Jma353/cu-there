import json
from . import *

namespace = '/venues'

@events.route(namespace + '/', methods=['GET'])
def get_venues():
  """
  Grab a sample list of venues
  """
  # Read file
  results = []
  with open('./1491102320.json') as f:
    results.extend(json.load(f))

  # Get unique venues
  venues = []; ids = set()
  for r in results:
    venue = r['venue']
    if venue['id'] not in ids:
      ids.add(venue['id'])
      venues.append(venue)

  result = {
    'success': True,
    'data': {
      'venues': venues
    }
  }

  return jsonify(result)
