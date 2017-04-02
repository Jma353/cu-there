import React, { Component } from 'react'
import Navigation from './navigation/Navigation'
require('../../public/sass/main.scss')

/**
 * Main application component.
 */
class App extends Component {

  /**
   * Render
   */
  render () {
    return (
      <div>
        <Navigation />
      </div>
    )
  }

}

export default App
