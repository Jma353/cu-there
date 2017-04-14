import React from 'react';
import { Route, IndexRoute } from 'react-router';

/* Routes */
import App from './components/App';
import Home from './components/pages/Home';
import Results from './components/pages/Results';

/* Routing scheme */
export default (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
    <Route path='results' component={Results} />
  </Route>
);
