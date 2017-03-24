import React, { Component } from 'react';
import SignIn from './SignIn';
import NavBar from './navigation/NavBar';
require('../../public/sass/main.scss');

/**
 * Main application component.
 */
class App extends Component {

  /**
   * Render 
   */
  render() {
    return (
      <div>
        <NavBar />
        <SignIn />
      </div>
    );
  }


}

export default App;
