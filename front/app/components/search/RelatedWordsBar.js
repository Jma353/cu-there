import React from 'react';
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
    this.state = {
      used: [],
      unused: []
    };
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
    this.setState({
      used: used,
      unused: unused
    });
  }

  /**
   * Handle remove a word from being used
   */
  handleRemoveWord (i) {
    let used = this.state.used.slice();
    let unused = this.state.unused.slice();
    unused.push(used.splice(i, 1));
    this.setState({
      used: used,
      unused: unused
    });
  }

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


  }
}

export default RelatedWordsBar;
