/**
 * The various aspects of state and relevance feedback
 * we take into account and store per query
 */
let initialSearchState = {
  query: '',
  categories: [],
  results: {
    response: {
      eventNames: [],
      venues: [],
      tags: [],
      times: [],
      graphs: []
    },
    events: {
      all: [],
      relevant: [],
      irrelevant: []
    }
  }
};

/**
 * Search reducer
 */
export function _search (state = initialSearchState, action) {
  switch (action.type) {
    case 'DID_SEARCH_SUCCESS':
      return action.result;
    case 'DID_CHANGE_RELEVANCE_SUCCESS':
      return action.result;
    default:
      return state;
  }
}
