import React, { Component } from 'react'
import Navigation from './navigation/Navigation'
import Footer from './navigation/Footer'
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
        <Footer />
      </div>
    )
  }

}

export default App
