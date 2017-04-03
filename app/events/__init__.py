from flask import Blueprint
from app import *

# Events Blueprint
events = Blueprint('events', __name__, url_prefix='/events')

# Import all endpoints
from controllers.venues_controller import *
