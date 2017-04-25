import React from 'react';
import axios from 'axios';

require('../../../public/sass/CategoryBar.scss');

import SuggestionList from '../lists/SuggestionList';

class CategoryBar extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      available: [],
      value: null,
      suggestions: [],
      suggestionIndex: 0
    };
  }

  componentDidMount () {
    axios.get('/categories')
      .then(resp => {
        const categories = resp.data.data.categories;
        this.setState({
          available: categories,
          suggestions: categories
        });
      });
  }

  /**
   * Handle add input
   */
  handleAdd () {
    this.setState({
      value: ''
    });
  }

  /**
   * Handle change input
   */
  handleChange (e) {
    this.setState({
      value: e.target.value,
      suggestions: this.state.available.filter((c) =>
        c.toLowerCase().startsWith(e.target.value)
      ),
      suggestionIndex: 0
    });
  }

  /**
   * Handle unfocus input
   */
  handleBlur (e) {
    this.setState({
      value: null,
      suggestions: this.state.available,
      suggestionIndex: 0
    });
  }

  /**
   * Handle keydown for enter and arrow keys
   */
  handleKeyDown (event) {
    const { suggestionIndex, suggestions } = this.state;

    if (event.keyCode === 37 || event.keyCode === 39) {
      this.setState({
        suggestions: [],
        suggestionIndex: 0
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

      if (newIndex < 0) newIndex = 0;
      if (newIndex >= suggestions.length) newIndex = suggestions.length - 1;

      this.setState({
        suggestionIndex: newIndex
      });
    }
  }

  /**
   * Handle submit
   */
  handleSubmit (e) {
    if (this.state.suggestionIndex !== 0) {
      console.log('yeah');
    }
  }

  /**
   * Handle select suggestion
   */
  handleSelectSuggestion (i) {
    if (this.state.suggestions.length !== 0) {
      this.props.onAdd(this.state.suggestions[i]);
      this.setState({
        value: null,
        suggestions: this.state.available,
        suggestionIndex: 0
      });
    }
  }

  render () {
    const categories = this.props.categories.map((c, i) =>
      <li className='category-item' key={i}>
        <span>{c}</span>
        <button className='fa fa-times' onClick={() => this.props.onCategoryDelete(i)} />
      </li>
    );

    const addCategory = this.state.value === null
      ? (
        <li className='category-item category-add' onClick={() => this.handleAdd()}>
          <button className='fa fa-plus' />
          <span>Add Category</span>
        </li>
      ) : (
        <li className='category-item category-add' onClick={() => this.handleAdd()}>
          <button className='fa fa-plus' />
          <input
            autoFocus
            value={this.state.value}
            onChange={(e) => this.handleChange(e)}
            placeholder={'Category'}
            onKeyDown={(e) => this.handleKeyDown(e)}
            onBlur={(e) => this.handleBlur(e)}
            />
          {
            this.state.value !== null &&
            this.state.suggestions.length !== 0 &&
            <SuggestionList
              retainQuery
              query={this.state.value}
              suggestions={this.state.suggestions.slice(0, 6)}
              selectedIndex={this.state.suggestionIndex}
              onItemClick={(i) => this.handleSelectSuggestion(i)}
              />
          }
        </li>
      );

    return (
      <div className='category-bar'>
        <span className='category-label'>Categories:</span>
        <ul className='category-list'>
          {categories}
          {addCategory}
        </ul>
      </div>
    );
  }
}

export default CategoryBar;
