import React from 'react';
import VenueCard from './VenueCard';
require('../../public/sass/VenueList.scss');

class VenueList extends React.Component {

  generateCard (venue, i) {
    return <VenueCard data={venue} key={i} />;
  }

  /**
   * render
   */
  render () {
    let venues = this.props.venues.map(this.generateCard);
    return (
      <div className='venue-list'>
        {venues}
      </div>
    );
  }
}

export default VenueList;
