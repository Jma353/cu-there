import React from 'react';
import Navigation from './navigation/Navigation';
import Footer from './navigation/Footer';
require('../../public/sass/App.scss');

/**
 * Main application component.
 */
class App extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div>
        <Navigation />
        <Footer />
      </div>
    );
  }

}

export default App;
