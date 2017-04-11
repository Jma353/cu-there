import React from 'react';
require('../../../public/sass/VenueCard.scss');

/**
 * A card to display basic info about a venue
 */
class VenueCard extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='venue-card'>
        <div className='venue-info-item'>
          {this.props.data.name}
        </div>
        <div className='venue-img-item'>
          <img src={this.props.data.profile_picture} />
        </div>
      </div>
    );
  }
}

export default VenueCard;
