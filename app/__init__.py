# Imports
import os
import dill
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from preprocessing.preprocess import Preprocess

# Configure app
app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

# Preprocess matrices and such
preprocessed = None
if os.path.isfile('preprocessed.p'):
  preprocessed = dill.load(open('preprocessed.p', 'rb'))
else:
  preprocessed = Preprocess()
  dill.dump(preprocessed, open('preprocessed.p', 'wb'))

# Import + Register Blueprints
from app.events import events as events
app.register_blueprint(events)

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

# Data
import store
store.store_venues('events.json', db)
