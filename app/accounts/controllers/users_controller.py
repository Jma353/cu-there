from . import *

@accounts.route('/sign_in', methods=['POST'])
@google_sign_in
def sign_in(**kwargs):
  # Just spit back google credentials for now
  google_creds =  kwargs.get('google_creds', {})
  return jsonify(google_creds)
