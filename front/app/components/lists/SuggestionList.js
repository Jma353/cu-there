import React from 'react';

class SuggestionList extends React.Component {
  render () {
    const items = this.props.suggestions
    .filter((s) => this.props.query !== s).map((s, i) => {
      const className = i === this.props.selectedIndex
        ? 'selected'
        : 'unselected';

      const prefix = this.props.query.split(' ');
      const lastWord = prefix.splice(-1)[0];

      var lastWordStart = null;
      var lastWordRemainder = s;

      if (s.startsWith(lastWord)) {
        lastWordStart = lastWord;
        lastWordRemainder = s.slice(lastWord.length);
      }

      return (
        <li key={i} className={className} onClick={() => this.props.onItemClick(i)}>
          <span>{prefix.join(' ')} {lastWordStart}<b>{lastWordRemainder}</b></span>
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
