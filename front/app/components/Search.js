import React, { Component } from 'react'
import {
  Jumbotron
} from 'React-Bootstrap'

/**
 * Parent component containing the SearchBar and ContextSwitcher.
 */
class Search extends Component {
  render () {
    return (
      <Jumbotron className='text-center'>
        <h1>Hello world!</h1>
        <p>Welcome to CU There!</p>
      </Jumbotron>
    )
  }
}

export default Search
