import React from 'react';
require('../../../public/sass/RelatedWordsCell.scss');

/**
 * Cell containing info about related words
 */
class RelatedWordsCell extends React.Component {

  /**
   * Render
   */
  render () {
    // Used or unused cell
    const cell = this.props.used
      ? (
        <li className='related-words-item related-words-used'>
          <span>{this.props.word}</span>
          <button
            className='fa fa-times'
            onClick={() => { this.props.handleRemove(this.props.id); }} />
        </li>
      ) : (
        <li
          className='related-words-item related-words-unused'
          onClick={() => { this.props.handleUse(this.props.id); }}>
          <span>{this.props.word}</span>
        </li>
      );

    return cell;
  }
}

export default RelatedWordsCell;
