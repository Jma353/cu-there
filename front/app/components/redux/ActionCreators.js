// TODO - ajax requesting


/**
 * Did search for results with query `query
 */
export function didSearch (query) {
  return {
    type: 'DID_SEARCH',
    query: query
  };
}

/**
 * Did change relevance -> query again with modified
 * `relevant` / `irrelevant` information
 */
export function didChangeRelevance (query, relevant, irrelevant) {
  return {
    type: 'DID_CHANGE_RELEVANCE',
    relevant: relevant,
    irrelevant: irrelevant
  };
}
