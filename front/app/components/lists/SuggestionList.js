import React from 'react';

class SuggestionList extends React.Component {
  render () {
    const items = this.props.suggestions.map((s, i) => {
      const className = i === this.props.selectedIndex
        ? 'selected'
        : 'unselected';

      const prefix = this.props.query.split(' ');
      prefix.splice(-1);

      return (
        <li key={i} className={className} onClick={() => this.props.onItemClick(i)}>
          <span>{prefix.join(' ')} <b>{s}</b></span>
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
