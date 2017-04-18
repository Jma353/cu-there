import util from 'util';
import axios from 'axios';
import Promise from 'bluebird';

/**
 * Did search for results with query `query
 */
export function didSearch (query) {
  return {
    types: ['DID_SEARCH_REQUEST', 'DID_SEARCH_SUCCESS', 'DID_SEARCH_FAILURE'],
    promise: () => {
      return axios.get('/search?q=' + encodeURIComponent(query))
        .then(resp => {
          return Promise.resolve({
            query: query,
            results: {
              response: {
                venues: resp.data.venues,
                tags: resp.data.tags,
                times: resp.data.times
              },
              events: {
                relevant: resp.data.relevant,
                irrelevant: resp.data.irrelevant
              }
            }
          });
      });
    }
  };
}

/**
 * Did change relevance -> query again with modified
 * `relevant` / `irrelevant` information
 */
export function didChangeRelevance (query, relevant, irrelevant) {
  return {
    types: ['DID_CHANGE_RELEVANCE_REQUEST', 'DID_CHANGE_RELEVANCE_SUCCESS', 'DID_CHANGE_RELEVANCE_FAILURE'],
    promise: () => {
      return axios.get(util.format(
        '/search/rocchio?q=%s&relevant=%s&irrelevant=%s',
        encodeURIComponent(query),
        encodeURIComponent(relevant),
        encodeURIComponent(irrelevant)))
        .then(resp => {
          return Promise.resolve({
            query: query,
            results: {
              response: {
                venues: resp.data.venues,
                tags: resp.data.tags,
                times: resp.data.times
              },
              events: {
                relevant: resp.data.relevant,
                irrelevant: resp.data.irrelevant
              }
            }
          });
      });
    }
  };
}
