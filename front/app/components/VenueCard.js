import React from 'react';
require('../../public/sass/VenueCard.scss');

class VenueCard extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='venue-card'>
        <div className='venue-info sm-text'>
          {this.props.data.name}
        </div>
        <div className='venue-img'>
          <img src={this.props.data.profile_picture} />
        </div>
      </div>
    );
  }

}

export default VenueCard;
