# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from preprocessing.preprocess import Preprocess

# Configure app
socketio = SocketIO()
app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

# Preprocessing
preprocessed = Preprocess()

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
