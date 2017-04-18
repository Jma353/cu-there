import React from 'react';

require('../../../public/sass/Search.scss');

import LightButton from '../buttons/LightButton.js';
require('../../../public/sass/LightButton.scss');

/**
 * Defines a generic Search component
 * that can be reused throughout the app
 */
class Search extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.state = { value: '' };
    // Placeholders for now
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  /**
   * Handle a change to text input
   */
  handleChange (event) {
    this.setState({ value: event.target.value });
  }

  /**
   * Handle submission of search query
   */
  handleSubmit (event) {
    console.log('A search was made ' + this.state.value);
    window.location.href = `/results?query=${this.state.value}`
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='search'>
        {/* The bar itself */}
        <input type='text'
          value={this.state.value}
          onChange={this.handleChange}
          placeholder={this.props.placeholder || ''}
          className='bar' />
        {/* Submit button */}
        <LightButton className='submit' onClick={this.handleSubmit}>
          GO
        </LightButton>
      </div>
    );
  }
}

export default Search;
