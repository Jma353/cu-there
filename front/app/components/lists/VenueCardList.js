import React from 'react';
import VenueCard from '../cards/VenueCard';
import generateCardList from './generateCardList';
require('../../../public/sass/VenueCardList.scss');

class VenueCardList extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='venue-card-list-container'>
        <div className='venue-card-list-title'>
          {this.props.title}
        </div>
        <div className='venue-card-list'>
          {this.props.cards}
        </div>
      </div>
    );
  }
}

export default generateCardList(VenueCardList, VenueCard);
