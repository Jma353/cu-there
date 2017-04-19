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
  console.log(action);
  switch (action.type) {
    case 'DID_SEARCH_SUCCESS':
      return action.result;
    case 'DID_CHANGE_RELEVANCE_SUCCESS':
      return action.result;
    default:
      return state;
  }
}
