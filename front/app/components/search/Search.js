import React from 'react';

require('../../../public/sass/Search.scss');

import LightButton from '../buttons/LightButton';
require('../../../public/sass/LightButton.scss');

import DarkButton from '../buttons/DarkButton';
require('../../../public/sass/DarkButton.scss');

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

  componentDidMount () {
    const socket = require('socket.io-client')('/search');
    const uuid = getUUID();
    console.log(uuid);

    socket.on('connect', () => {
      console.log('Search socket connected.');
    });

    socket.on(uuid, (data) => {
      console.log('search:', data);
    });

    socket.on('disconnect', () => {
      console.log('Search socket disconnected.');
    });

    this._socket = socket;
  }

  /**
   * Handle a change to text input
   */
  handleChange (event) {
    const value = event.target.value;
    this.setState({ value: value });
    this._socket.emit('search', value);
  }

  /**
   * Handle submission of search query
   */
  handleSubmit (event) {
    if (this.state.value) window.location.href = `/results?q=${this.state.value}`;
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
    const submitButton = this.props.light
      ? <LightButton className='submit fa fa-search' onClick={this.handleSubmit} />
      : <DarkButton className='submit fa fa-search' onClick={this.handleSubmit} />;
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
        {submitButton}
      </div>
    );
  }
}

function getUUID () {
  function S4 () {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
  }
  return (S4() + S4() + '-' + S4() + '-4' + S4().substr(0, 3) + '-' + S4() + '-' + S4() + S4() + S4()).toLowerCase();
}

export default Search;
