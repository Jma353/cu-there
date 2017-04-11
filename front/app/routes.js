import React from 'react';
import { Route, IndexRoute } from 'react-router';

/* Routes */
import App from './components/App';
import Home from './components/pages/Home';

/* Routing scheme */
export default (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
  </Route>
);
