import React, { Component } from 'react';
require('../../public/sass/main.scss');
import SignIn from './SignIn';

/**
 * Main application component.
 */
class App extends Component {
  render() {
    return (
      <div>
        <SignIn />
      </div>
    );
  }
}

export default App;
