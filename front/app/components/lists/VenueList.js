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
   * Set the detail view of the venue list
   */
  setDetail (detail) {
    this.setState({ detail: detail });
  }

  /**
   * Generate a venue card
   */
  generateCard (venue, i) {
    return <VenueCard data={venue} key={i} id={i} />;
  }

  /**
   * Render
   */
  render () {
    let venues = this.props.venues.map(this.generateCard);
    return (
      <div>
        <div className='venue-list'>
          {venues}
        </div>
      </div>
    );
  }
}

export default VenueList;
