import React from 'react';
import axios from 'axios';

require('../../../public/sass/Search.scss');

import SuggestionList from '../lists/SuggestionList';
import CategoryBar from './CategoryBar';
import RelatedWordsBar from './RelatedWordsBar';

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
    this.componentConfig(props, {});
  }

  componentConfig (data, relatedWords) {
    this.state = {
      value: data.initialValue || '',
      suggestions: [],
      suggestionIndex: -1,
      categories: data.initialCategories || [],
      usedRelatedWords: relatedWords.usedRelatedWords || [],
      unusedRelatedWords: relatedWords.unusedRelatedWords || []
    };
  }

  componentWillReceiveProps (nextProps) {
    // Arrays we're building
    let usedRelatedWords = [];
    let unusedRelatedWords = [];

    // Shorter names
    let initialRelatedWords = nextProps.initialRelatedWords || [];
    let relatedWords = nextProps.relatedWords || [];

    // Build used
    for (let i = 0; i < initialRelatedWords.length; i++) {
      if (relatedWords.includes(initialRelatedWords[i])) {
        usedRelatedWords.push(initialRelatedWords[i]);
      }
    }

    // Build unused
    for (let i = 0; i < relatedWords.length; i++) {
      if (!usedRelatedWords.includes(relatedWords[i])) {
        unusedRelatedWords.push(relatedWords[i]);
      }
    }
    this.componentConfig(
      nextProps, {
        usedRelatedWords: usedRelatedWords,
        unusedRelatedWords: unusedRelatedWords
      });
  }

  handleFreshSearch () {
    this.setState({
      usedRelatedWords: [],
      unusedRelatedWords: []
    }, () => {
      this.handleSubmit();
    });
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
        axios.get(`/info/autocomplete?query=${encodeURIComponent(query)}`)
          .then(resp => {
            this.setState({
              suggestions: resp.data.data.suggestions.slice(0, 6)
            });
          });
      }
    }
  }

  /**
   * Handle submission of search query
   */
  handleSubmit () {
    if (this.state.value) {
      window.location.href = `/results?q=${this.state.value}&categs=${this.state.categories}&related_words=${this.state.usedRelatedWords}`;
    }
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
      if (suggestionIndex < 0) this.handleFreshSearch();
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

  /**
   * Handle suggestion selection by mouse or by keystroke
   */
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

  /**
   * Handle unfocusing search
   */
  handleBlur (e) {
    this.setState({
      suggestions: [],
      suggestionIndex: -1
    });
  }

  // MARK - Handle category operations

  /**
   * Handle add category
   */
  handleCategoryAdd (c) {
    this.setState({
      categories: this.state.categories.concat([c])
    }, () => {
      this.handleSubmit();
    });
  }

  /**
   * Handle add category
   */
  handleCategoryDelete (i) {
    const { categories } = this.state;
    categories.splice(i, 1);
    this.setState({
      categories: categories
    }, () => {
      this.handleSubmit();
    });
  }

  // MARK - Handle related word use / removal

  /**
   * Handle use a word
   */
  handleUseRelatedWord (i) {
    let used = this.state.usedRelatedWords.slice();
    let unused = this.state.unusedRelatedWords.slice();
    used.push(unused.splice(i, 1));
    this.setState({
      usedRelatedWords: used,
      unusedRelatedWords: unused
    }, () => {
      this.handleSubmit();
    });
  }

  /**
   * Handle remove a word from being used
   */
  handleRemoveRelatedWord (i) {
    let used = this.state.usedRelatedWords.slice();
    let unused = this.state.unusedRelatedWords.slice();
    unused.push(used.splice(i, 1));
    this.setState({
      usedRelatedWords: used,
      unusedRelatedWords: unused
    }, () => {
      this.handleSubmit();
    });
  }

  /**
   * Render
   */
  render () {
    const buttonProps = {
      className: 'submit fa fa-search',
      onClick: () => {
        this.handleFreshSearch();
      }
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
            onBlur={(e) => this.handleBlur(e)}
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
        {/* Related Words Picker Bar */}
        <RelatedWordsBar
          used={this.state.usedRelatedWords}
          unused={this.state.unusedRelatedWords}
          handleUseWord={(i) => { this.handleUseRelatedWord(i); }}
          handleRemoveWord={(i) => { this.handleRemoveRelatedWord(i); }}
          />
        {/* Category Selection Bar */}
        <CategoryBar
          categories={this.state.categories}
          availableCategories={this.props.availableCategories}
          onDelete={(i) => this.handleDelete(i)}
          onAdd={(c) => this.handleCategoryAdd(c)}
          onCategoryDelete={(i) => this.handleCategoryDelete(i)}
          />
      </div>
    );
  }
}

export default Search;
