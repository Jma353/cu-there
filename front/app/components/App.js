import React, { Component } from 'react'
import Navigation from './navigation/Navigation'
import Footer from './navigation/Footer'
import Search from './Search'
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
        <Search />
        <Footer />
      </div>
    )
  }

}

export default App
