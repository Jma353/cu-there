import React from 'react';
import TextCard from '../cards/TextCard';
import generateCardList from './generateCardList';
require('../../../public/sass/TextCardList.scss');

class TextCardList extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='text-card-list-container'>
        <div className='text-card-list-title'>
          <h2>{this.props.title}</h2>
        </div>
        <div className='text-card-list-content'>
          {this.props.cards}
        </div>
      </div>
    );
  }
}

export default generateCardList(TextCardList, TextCard);
