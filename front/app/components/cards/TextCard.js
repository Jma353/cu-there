import React from 'react';
require('../../../public/sass/TextCard.scss');

/**
 * A card displaying purely text information
 */
class TextCard extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='text-card'>
        {this.props.text}
      </div>
    );
  }
}

export default TextCard;
