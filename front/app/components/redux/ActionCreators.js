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
                venues: resp.data.data.venues,
                tags: resp.data.data.tags,
                times: resp.data.data.times
              },
              events: {
                all: resp.data.data.events,
                relevant: resp.data.data.events.map(e => { return e.id; }),
                irrelevant: []
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
export function didChangeRelevance (query, relevant, irrelevant, all) {
  return {
    types: ['DID_CHANGE_RELEVANCE_REQUEST', 'DID_CHANGE_RELEVANCE_SUCCESS', 'DID_CHANGE_RELEVANCE_FAILURE'],
    promise: () => {
      let relS = relevant.map(r => { return '&relevent=' + r; });
      let irrelS = irrelevant.map(ir => { return '&irrelevant=' + ir; });
      return axios.get(util.format(
        '/search/rocchio?q=%s%s%s',
        encodeURIComponent(query), relS, irrelS))
        .then(resp => {
          return Promise.resolve({
            query: query,
            results: {
              response: {
                venues: resp.data.data.venues,
                tags: resp.data.data.tags,
                times: resp.data.data.times
              },
              events: {
                all: all,
                relevant: relevant,
                irrelevant: irrelevant
              }
            }
          });
        });
    }
  };
}
