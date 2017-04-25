import React from 'react';

require('../../../public/sass/Search.scss');

import SuggestionList from '../lists/SuggestionList';
import CategoryBar from './CategoryBar';

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
      suggestionIndex: -1,
      categories: []
    };
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
        suggestions: data.slice(0, 6)
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
      const query = value.split(' ').splice(-1)[0];
      this.setState({ value: value });

      if (query === '') {
        this.setState({
          suggestions: [],
          suggestionIndex: -1
        });
      } else {
        const req = {
          session: this._uuid,
          query: query
        };
        this._socket.emit('search', JSON.stringify(req));
      }
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
    const { suggestionIndex, suggestions } = this.state;

    if (event.keyCode === 37 || event.keyCode === 39) {
      this.setState({
        suggestions: [],
        suggestionIndex: -1
      });
    }

    if (event.key === 'Enter') {
      if (suggestionIndex < 0) this.handleSubmit(event);
      else {
        this.handleSelectSuggestion(suggestionIndex);
      }
    } else {
      var newIndex = suggestionIndex;
      // Up
      if (event.keyCode === 38) {
        newIndex--;
        event.preventDefault();
      }

      // Down
      if (event.keyCode === 40) {
        newIndex++;
        event.preventDefault();
      }

      if (newIndex < -1) newIndex = -1;
      if (newIndex >= suggestions.length) newIndex = suggestions.length - 1;

      this.setState({
        suggestionIndex: newIndex
      });
    }
  }

  handleSelectSuggestion (i) {
    const word = this.state.suggestions[i] + ' ';
    const lastSpaceIndex = this.state.value.lastIndexOf(' ') + 1;
    const newValue = this.state.value.slice(0, lastSpaceIndex) + word;
    this.setState({
      value: newValue,
      suggestions: [],
      suggestionIndex: -1
    });
  }

  handleBlur () {
    this.setState({
      suggestions: [],
      suggestionIndex: -1
    });
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
      <div className='search-container'>
        <div className='search'>
          {/* The bar itself */}
          <input type='text'
            value={this.state.value}
            onChange={(e) => this.handleChange(e)}
            placeholder={'e.g. A tech talk hosted by ACSU'}
            className='bar'
            onKeyDown={(e) => this.handleKeyDown(e)}
            onBlur={() => this.handleBlur()}
            />
          {/* Submit button */}
          {submitButton}
          {this.state.suggestions.length !== 0
            ? <SuggestionList
              query={this.state.value}
              suggestions={this.state.suggestions}
              selectedIndex={this.state.suggestionIndex}
              onItemClick={(i) => this.handleSelectSuggestion(i)}
              /> : null}
        </div>
        <CategoryBar
          categories={this.state.categories}
          availableCategories={this.props.availableCategories}
          onDelete={(i) => this.handleDelete(i)}
          onAdd={(c) => this.onAdd(c)}
          />
      </div>
    );
  }
}

export default Search;
