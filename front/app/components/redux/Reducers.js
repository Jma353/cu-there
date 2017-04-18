/**
 * The various aspects of state and relevance feedback
 * we take into account and store per query
 */
let initialSearchState = {
  query: '',
  results: {
    response: {
      venues: [],
      tags: [],
      times: []
    },
    events: {
      relevant: [],
      irrelevant: []
    }
  }
};

/**
 * Search reducer
 */
export function _search (state = initialSearchState, action) {
  // TODO - handle various types of events
}
