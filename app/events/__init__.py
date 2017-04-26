from flask import Blueprint
from app import *

# Events Blueprint
events = Blueprint('events', __name__, url_prefix='')

# Import all endpoints
from controllers.search_controller import *
from controllers.info_controller import * 
