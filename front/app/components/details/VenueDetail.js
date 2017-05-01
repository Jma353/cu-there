import React from 'react';
require('../../../public/sass/VenueDetail.scss');

import { formatTime } from '../../utils/time.js';

/**
 * Displays abbreviated information about a venue (meant to
 * be used when displaying recommended venues after searching)
 */
class VenueDetail extends React.Component {

  /**
   * Render
   */
  render () {
    console.log(this.props.data.suggested_time);
    return (
      <div className='venue-detail-container'>
        {/* Image */}
        <div className='venue-detail-img'>
          <img src={this.props.data.profile_picture} />
        </div>
        <div className='venue-detail-text-container'>
          {/* Title */}
          <div className='venue-detail-title'>
            <a
              className='venue-detail-name'
              href={'http://maps.google.com/?q=' + this.props.data.latitude + ',' + this.props.data.longitude}
              target='_blank'>
              <strong>
                {this.props.data.name}
              </strong>
            </a> at {formatTime(this.props.data.suggested_time)}
          </div>
          {/* Address */}
          <div className='venue-detail-address'>
            <p>{this.props.data.street}</p>
            <p>{this.props.data.city}, {this.props.data.state} {this.props.data.zip}</p>
          </div>
          {/* Description */}
          <div className='venue-detail-description'>
            {this.props.data.about}
          </div>
          {/* Related events */}
          <div className='venue-detail-events'>
            <h3>Related Events</h3>
            {this.props.data.events.map((e, i) => {
              return (
                <p key={i}>{e.name}</p>
              );
            })}
          </div>
        </div>
      </div>
    );
  }
}

export default VenueDetail;
