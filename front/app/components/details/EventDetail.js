import React from 'react';

require('../../../public/sass/EventDetail.scss');

class EventDetail extends React.Component {
  render () {
    return (
      <div className='event-detail-container'>
        <div className='event-detail-img'>
          <img src={this.props.data.profile_picture} />
        </div>
        {/* Title */}
        <div className='event-detail-title'>
          {this.props.data.name}
        </div>
        {/* Venue */}
        <div className='event-detail-venue'>
          <p>{this.props.data.place.name}</p>
        </div>
        {/* Date */}
        <div className='event-detail-date'>
          <p>{this.props.data.date}</p>
        </div>
        {/* Description */}
        <div className='event-detail-description'>
          {this.props.data.description}
        </div>
        <button className='event-detail-dismiss fa fa-times' />
      </div>
    );
  }
}

export default EventDetail;
