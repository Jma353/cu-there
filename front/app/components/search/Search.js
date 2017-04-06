import React from 'react';
require('../../../public/sass/LightButton.scss');
require('../../../public/sass/Search.scss');

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
    // TODO
    this.setState({ value: event.target.value });
  }

  /**
   * Handel submission of search query
   */
  handleSubmit (event) {
    // TODO
    console.log('A search was made ' + this.state.value);
  }

  /**
   * Render
   */
  render () {
    return (
      <form onSubmit={this.handleSubmit} className='search'>
        {/* The bar itself */}
        <input type='text'
          value={this.state.value}
          onChange={this.handleChange}
          placeholder={this.props.placeholder || ''}
          className='bar' />
        {/* Submit button */}
        <input type='submit'
          value={this.props.submit}
          className='light-button submit' />
      </form>
    );
  }
}

export default Search;
