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
  switch (action.type) {
    case 'DID_SEARCH':
      return {
        ...state
      };
    case 'DID_CHANGE_RELEVANCE':
      return {
        ...state
      };
    default:
      return state;
  }
}
