from flask import request, render_template, jsonify
from functools import wraps
from app.events import events # Blueprint
