import { createStore, applyMiddleware, combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import promiseMiddleware from './PromiseMiddleware';
import * as reducers from './Reducers';

export default function (data) {
  var reducer = combineReducers({ ...reducers, routing: routerReducer });
  var finalCreateStore = applyMiddleware(promiseMiddleware)(createStore);
  var store = finalCreateStore(reducer, data);
  return store;
}
