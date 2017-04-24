# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
import json
import re
import numpy as np
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from flask import Flask, render_template, jsonify, make_response
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

def stem(terms):
  """
  Stem each word in word list using Porter Stemming Algorithm
  """
  stemmer = PorterStemmer()
  return [stemmer.stem(term) for term in terms]

def tokenize(text):
  """
  Tokenize text into list of words and stem words (also remove links and emails)
  """
  text = text.lower()

  emails_links_regex = re.compile(r'(((http|https)\:\/\/(([a-z|0-9]+)\.)*([a-z|0-9]+)\.([a-z|0-9]+)(\/([a-z|0-9]+))*))|([\w\.-]+@[\w\.-]+)')

  text = re.sub(emails_links_regex, '', text)

  return re.findall(r'[a-z]+', text)

def data_storage():
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
  tfidf_vec = TfidfVectorizer(tokenizer=tokenize, min_df=5, max_df=0.95, max_features=5000, stop_words='english')
  event_descs = [event["description"] for event in OUR_EVENTS]
  doc_by_term = tfidf_vec.fit_transform(event_descs).toarray()

  categs = [event["category"] for event in OUR_EVENTS]
  categ_to_event = defaultdict(list) # Dict format: {category: [events marked as category]}

  for idx, categ in enumerate(categs):
    if categ != "N/A":
      categ_to_event.setdefault(categ,[]).append(idx)

  uniq_categs = [c for c in categ_to_event.keys()]
  categ_name_to_idx = {name:idx for idx, name in enumerate(uniq_categs)}
  categ_idx_to_name = {v:k for k,v in categ_name_to_idx.items()}
  categ_by_term = np.empty([len(uniq_categs), len(doc_by_term[0])])

  # Build categ_by_term matrix
  for idx, _ in enumerate(categ_by_term):
    # Get event vectors for category
    categ = categ_idx_to_name[idx]
    event_vecs = [doc_by_term[event] for event in categ_to_event[categ]]

    # Calculate category average vector
    vec_sum = np.sum(event_vecs, axis=0)
    norm = np.linalg.norm(vec_sum)
    avg_tfidf_vec = vec_sum / float(norm)
    categ_by_term[idx,:] = avg_tfidf_vec

  print 'Loaded data-structures and data...'

  return OUR_EVENTS, tfidf_vec, doc_by_term, categ_by_term, categ_name_to_idx, tfidf_vec.get_feature_names()

# Grab info
OUR_EVENTS, tfidf_vec, doc_by_term, categ_by_term, categ_name_to_idx, features = data_storage()

# Import + Register Blueprints
from app.events import events as events
app.register_blueprint(events)

# Initialize app w/SocketIO
socketio.init_app(app)

# Default functionality of rendering index.html
def render_page():
  return render_template('index.html')

# React Catch All Paths
@app.route('/', methods=['GET'])
def index():
  return render_page()
@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
  return render_page()

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404
