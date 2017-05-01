import React from 'react';
import RelatedWordsCell from './RelatedWordsCell';
require('../../../public/sass/RelatedWordsBar.scss');

/**
 * Related words
 */
class RelatedWordsBar extends React.Component {

  /**
   * Generate a related word cell
   */
  generateCell (info, i) {
    const key = (info.used ? 'used' : 'unused') + i;
    return <RelatedWordsCell
      key={key}
      used={info.used}
      word={info.word}
      handleUse={this.props.handleUseWord}
      handleRemove={this.props.handleRemoveWord}
      id={i} />;
  }

  /**
   * Render
   */
  render () {
    let usedInfos = this.props.used.map(w => { return { word: w, used: true }; });
    let unusedInfos = this.props.unused.map(w => { return { word: w, used: false }; });
    let usedWordCells = usedInfos.map((info, i) => this.generateCell(info, i));
    let unusedWordCells = unusedInfos.map((info, i) => this.generateCell(info, i));
    return (
      <div className='related-words-bar'>
        <ul className='related-words-list'>
          {usedWordCells}
          {unusedWordCells}
        </ul>
      </div>
    );
  }
}

export default RelatedWordsBar;
