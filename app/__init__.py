# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
import json
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure app
socketio = SocketIO()
app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

################
# DATA STORAGE #
################

# DB
db = SQLAlchemy(app)

def data_storage():
  import store
  # Store everything
  store.store_venues('events.json', db)

  # Load events
  OUR_EVENTS = {}

  with open('events.json') as events_json:
    events_dict = json.load(events_json)

    # List of event dicts containing id, name, description, category
    OUR_EVENTS = [{'id': event['id'], 'name': event['name'],
                    'description': event['description'] if event['description'] else '',
                    'category': event['category'] if event['category'] else ''}
                     for event in events_dict]

  # Load in TF-IDF matrix (or compute if it's first time)
  tfidf_vec = TfidfVectorizer(min_df=5, max_df=0.95, max_features=5000, stop_words='english')
  event_descs = [event["description"] for event in OUR_EVENTS]
  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()

  print 'Loaded data-structures and data...'
  return OUR_EVENTS, tfidf_vec, event_descs, doc_by_term

# Grab info
OUR_EVENTS, tfidf_vec, event_descs, doc_by_term = data_storage()

# Import + Register Blueprints
from app.events import events as events
app.register_blueprint(events)

# Initialize app w/SocketIO
socketio.init_app(app)

# React Catch All Paths
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404
