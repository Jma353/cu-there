import React from 'react';
import axios from 'axios';
import RelatedWordsCell from './RelatedWordsCell';
require('../../../public/sass/RelatedWordsBar.scss');

/**
 * Related words
 */
class RelatedWordsBar extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.generateCell = this.generateCell.bind(this);
    this.handleUseWord = this.handleUseWord.bind(this);
    this.handleRemoveWord = this.handleRemoveWord.bind(this);
  }

  /**
   * Handle use a word
   */
  handleUseWord (i) {
    let used = this.state.used.slice();
    let unused = this.state.unused.slice();
    used.push(unused.splice(i, 1));
    // TODO - dispatch REDUX
  }

  /**
   * Handle remove a word from being used
   */
  handleRemoveWord (i) {
    let used = this.state.used.slice();
    let unused = this.state.unused.slice();
    unused.push(used.splice(i, 1));
    // TODO - dispatch REDUX
  }

  /**
   * Generate a related word cell
   */
  generateCell (info, i) {
    const key = (info.used ? 'used' : 'unused') + i;
    return <RelatedWordsCell
      key={key}
      used={info.used}
      word={info.word}
      handleUse={this.handleUseWord}
      handleRemove={this.handleRemoveWord}
      id={i} />;
  }

  /**
   * Render
   */
  render () {
    let usedInfos = this.props.used.map(w => { return { word: w, used: true }; });
    let unusedInfos = this.props.unused.map(w => { return { word: w, used: false }; });
    let usedWordsCells = usedInfos.map(this.generateCell);
    let unusedWordsCells = usedInfo
  }
}

export default RelatedWordsBar;
