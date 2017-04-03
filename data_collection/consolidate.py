import json
import time
import os

def consolidate_jsons(dirr):
  # Grab the json files
  jsons = []
  for _, _, filenames in os.walk('../{1}'.replace('{1}', dirr)):
    jsons.extend([f for f in filenames if 'json' in f])

  # Built resultant + book-keeping
  events = []
  seen_ids = set()

  # Go through all existing JSONs
  for j in jsons:

    # Grab the JSON info
    results = None
    with open('../{1}/{2}'.replace('{1}', dirr).replace('{2}', j)) as infile:
      results = json.load(infile)

    # Differentiates between previously consolidated
    # files + results from the Facebook API
    results = results if 'events' not in results else results['events']

    # Add to the resultant
    for e in results:
      if e['id'] not in seen_ids:
        seen_ids.add(e['id'])
        events.append(e)

  # Output our consolidation
  secs = str(int(round(time.time())))
  file_name = str(secs) + '-consolidation.json'
  with open('../{1}/{2}'.replace('{1}', dirr).replace('{2}', file_name), 'w') as outfile:
    json.dump(events, outfile)


# Run the actual function
consolidate_jsons('results')
