import json
from . import *

namespace = '/venues'

@events.route(namespace + '/', methods=['GET'])
def get_venues():
  """
  Grab a sample list of venues
  """
  
  result = {
    'success': True,
    'data': {
      'venues': []
    }
  }

  return jsonify(result)
