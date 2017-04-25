import json
from . import *
from app.events.models import queries

namespace = '/categories'

@events.route(namespace + '/', methods=['GET'])
def get_categories():
  """
  Grab a list of all categories from database events
  """
  categories = app.preprocessed.uniq_categs
  categories = [venue_schema.dump(c).data for c in categories]

  result = {
    'success': True,
    'data': {
      'categories': categories
    }
  }

  return jsonify(result)
