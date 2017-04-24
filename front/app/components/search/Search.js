import React from 'react';

require('../../../public/sass/Search.scss');

import SuggestionList from '../lists/SuggestionList';

import LightButton from '../buttons/LightButton';
require('../../../public/sass/LightButton.scss');

import DarkButton from '../buttons/DarkButton';
require('../../../public/sass/DarkButton.scss');

import getUUID from '../../utils/uuid';

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
    this.state = {
      value: this.props.initialValue,
      suggestions: [],
      selectedIndex: -1
    };
    // Placeholders for now
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
  }

  componentDidMount () {
    const socket = require('socket.io-client')('/search');
    const uuid = getUUID();

    socket.on('connect', () => {
      console.log('Search socket connected.');
    });

    socket.on('connect_error', (err) => {
      console.log(err);
    });

    socket.on(uuid, (data) => {
      this.setState({
        suggestions: data.slice(0, 8)
      });
    });

    socket.on('disconnect', () => {
      console.log('Search socket disconnected.');
    });

    this._socket = socket;
    this._uuid = uuid;
  }

  componentWillUnmount () {
    this._socket.close();
  }

  /**
   * Handle a change to text input
   */
  handleChange (event) {
    const value = event.target.value;

    if (!value) {
      this.setState({
        value: value,
        suggestions: []
      });
    } else {
      this.setState({ value: value });
      const query = value.split(' ').splice(-1)[0];
      console.log(query);
      const req = {
        session: this._uuid,
        query: query
      };
      this._socket.emit('search', JSON.stringify(req));
    }
  }

  /**
   * Handle submission of search query
   */
  handleSubmit (event) {
    if (this.state.value) window.location.href = `/results?q=${this.state.value}`;
  }

  /**
   * Handle key down
   */
  handleKeyDown (event) {
    const { selectedIndex, suggestions } = this.state;

    if (event.keyCode === 37 || event.keyCode === 39) {
      this.setState({
        suggestions: [],
        selectedIndex: -1
      });
    }

    if (event.key === 'Enter') {
      if (selectedIndex < 0) this.handleSubmit(event);
      else {
        const word = this.state.suggestions[selectedIndex] + ' ';
        const lastSpaceIndex = this.state.value.lastIndexOf(' ') + 1;
        const newValue = this.state.value.slice(0, lastSpaceIndex) + word;
        this.setState({
          value: newValue,
          suggestions: [],
          selectedIndex: -1
        });
      }
    } else {
      var newIndex = selectedIndex;
      // Up
      if (event.keyCode === 38) {
        newIndex--;
      }

      // Down
      if (event.keyCode === 40) {
        newIndex++;
      }

      if (newIndex < -1) newIndex = -1;
      if (newIndex >= suggestions.length) newIndex = suggestions.length - 1;

      this.setState({
        selectedIndex: newIndex
      });
    }
  }

  /**
   * Render
   */
  render () {
    const buttonProps = {
      className: 'submit fa fa-search',
      onClick: this.handleSubmit
    };

    const submitButton = this.props.light
      ? <LightButton {...buttonProps} />
      : <DarkButton {...buttonProps} />;

    return (
      <div className='search'>
        {/* The bar itself */}
        <input type='text'
          value={this.state.value}
          onChange={this.handleChange}
          placeholder={'e.g. A tech talk hosted by ACSU'}
          className='bar'
          onKeyDown={this.handleKeyDown} />
        {/* Submit button */}
        {submitButton}
        {this.state.suggestions.length !== 0
          ? <SuggestionList
            suggestions={this.state.suggestions}
            selectedIndex={this.state.selectedIndex}
            /> : null}
      </div>
    );
  }
}

export default Search;
