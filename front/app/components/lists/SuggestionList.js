import React from 'react';

require('../../../public/sass/SuggestionList.scss');

class SuggestionList extends React.Component {
  render () {
    const items = this.props.suggestions
      .filter((s) => this.props.query !== s || this.props.retainQuery)
      .map((s, i) => {
        const className = i === this.props.selectedIndex
          ? 'selected'
          : 'unselected';

        const prefix = this.props.query.split(' ');
        const lastWord = prefix.splice(-1)[0].toLowerCase();

        var lastWordStart = null;
        var lastWordRemainder = s;

        if (s.toLowerCase().startsWith(lastWord)) {
          lastWordStart = s.slice(0, lastWord.length);
          lastWordRemainder = s.slice(lastWord.length);
        }

        return (
          <li key={i} className={className} onMouseDown={() => this.props.onItemClick(i)}>
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
