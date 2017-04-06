import React from 'react';
import Detail from '../details/Detail';
require('../../../public/sass/VenueCard.scss');

/**
 * A card to display basic info about a venue
 */
class VenueCard extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  /**
   * Handle clicking card and displaying
   * venue details
   */
  handleClick (event) {
    event.preventDefault();
    console.log(event.currentTarget.getBoundingClientRect());
    let rect = event.currentTarget.getBoundingClientRect();
    let detail = <Detail x={(rect.left + rect.right) / 2} y={rect.bottom} />;
    this.props.setDetail(detail);
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='venue-card-container' onClick={this.handleClick}>
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
