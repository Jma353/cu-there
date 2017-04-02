import React from 'react';
require('../../public/sass/Search.scss');

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

  handleChange (event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit (event) {
    console.log('A search was made ' + this.state.value);
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='search'>
        <form onSubmit={this.handleSubmit} className='form'>
          {/* The bar itself */}
          <input type='text'
            value={this.state.value}
            onChange={this.handleChange}
            placeholder={this.props.placeholder || ''}
            className='bar' />
          {/* Recommend button */}
          <input type='submit'
            value={this.props.submit}
            className='button submit' />
        </form>
      </div>
    );
  }
}

export default Search;
