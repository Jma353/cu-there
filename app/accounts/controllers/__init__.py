from functools import wraps
from flask import request, jsonify, abort
from apiclient import discovery
from oauth2client import client
import httplib2
import os

# Import module models
from app.accounts.models.user import *
from app.accounts.models.session import *

# Blueprint for routing
from app.accounts import accounts

def google_sign_in(f):
  """Google sign in decorator for authenticating requests"""
  @wraps(f)
  def decorated_function(*args, **kwargs):

    # If this request does not have `X-Requested-With`
    # header, this could be a CSRF
    print request.headers
    if not request.headers.get('X-Requested-With'):
      abort(403)

    # Set path to the Web application client_secret_*.json
    # file downloaded from the Google API Console:
    # https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = os.environ['GOOGLE_CREDS_PATH']

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
      CLIENT_SECRET_FILE, ['profile', 'email'], request.get_json()['code'])

    google_creds = {
      'access_token': credentials.access_token,
      'refresh_token': credentials.refresh_token,
      'token_expiry': int(credentials.token_expiry.strftime('%s')),
      'id_token': credentials.id_token['sub'],
      'email': credentials.id_token['email']
    }
    # Return result of the function with appropriate values added
    return f(google_creds=google_creds, *args, **kwargs)

  return decorated_function
