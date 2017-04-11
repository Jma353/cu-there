import React from 'react';
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
        {this.props.children}
      </div>
    );
  }
}

export default App;
