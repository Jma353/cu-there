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
    this.state = { value: this.props.initialValue };
    // Placeholders for now
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
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
    window.location.href = `/results?q=${this.state.value}`;
  }

  /**
   * Handle key press for enter
   */
  handleKeyPress (event) {
    if (event.key === 'Enter') {
      this.handleSubmit(event);
    }
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
          placeholder={'e.g. A tech talk hosted by ACSU'}
          className='bar'
          onKeyPress={this.handleKeyPress} />
        {/* Submit button */}
        <LightButton className='submit fa fa-search' onClick={this.handleSubmit} />
      </div>
    );
  }
}

export default Search;
