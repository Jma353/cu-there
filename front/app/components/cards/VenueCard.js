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
      <a className='venue-card' href={'http://maps.google.com/?q=' + this.props.data.latitude + ',' + this.props.data.longitude} target='_blank'>
        <div className='venue-img-item'>
          <img src={this.props.data.profile_picture} />
        </div>
        <div className='venue-info-item'>
          {this.props.data.name}
        </div>
        <div className='venue-info-address'>
          {this.props.data.street}<br/>
          {this.props.data.city}, {this.props.data.state} {this.props.data.zip}
        </div>
      </a>
    );
  }
}

export default VenueCard;
