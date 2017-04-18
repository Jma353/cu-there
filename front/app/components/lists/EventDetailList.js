import React from 'react';

import EventDetail from '../details/EventDetail';
require('../../../public/sass/EventDetailList.scss');

class EventDetailList extends React.Component {
  constructor (props) {
    super(props);
    this.generateDetailList = this.generateDetailList.bind(this);
  }

  generateDetailList (event, i) {
    return <EventDetail data={event} key={i} />;
  }

  render () {
    const events = this.props.data.map(this.generateDetailList);

    return (
      <div className='event-detail-list-container'>
        <div className='event-detail-list-title'>{this.props.title}</div>
        <div className='event-detail-list-elements'>
          {events}
        </div>
      </div>
    );
  }
}

export default EventDetailList;
