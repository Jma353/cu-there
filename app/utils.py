import requests as r
import urllib
import os

def get_app_access_token():
  """
  Grabs FB access token to our `cu-there` app
  Returns: access token as a string
  """
  params = {
    'client_id' : os.environ['FB_CLIENT_ID'],
    'client_secret' : os.environ['FB_CLIENT_SECRET'],
    'grant_type' : 'client_credentials'
  }
  base_url = "https://graph.facebook.com/oauth/access_token?"
  result = r.post(base_url + urllib.urlencode(params))
  return result.text[(result.text.rfind('=')+1):]
