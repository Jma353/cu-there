import React from 'react';

class SuggestionList extends React.Component {
  render () {
    const items = this.props.suggestions.map((s, i) => {
      const className = i === this.props.selectedIndex
        ? 'selected'
        : 'unselected';
      return (
        <li key={i} className={className}>
          <span>{s}</span>
        </li>
      );
    });

    return (
      <div className='suggestion-list'>
        <ul>
          {items}
        </ul>
      </div>
    );
  }
}

export default SuggestionList;
