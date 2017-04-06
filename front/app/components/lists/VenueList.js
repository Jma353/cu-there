import React from 'react';
import VenueCard from '../cards/VenueCard';
require('../../../public/sass/VenueList.scss');

class VenueList extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.generateCard = this.generateCard.bind(this);
  }

  /**
   * Generate a venue card
   */
  generateCard (venue, i) {
    return <VenueCard data={venue} key={i} setDetail={this.props.setDetail} />;
  }

  /**
   * Render
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
