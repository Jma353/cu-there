import json
from . import *
from app.events.models import queries

# Serialization
event_schema = EventSchema()
venue_schema = VenueSchema()

namespace = '/venues'

@events.route(namespace + '/', methods=['GET'])
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
