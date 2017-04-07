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
    this.state = {};
    this.handleMouseEnter = this.handleMouseEnter.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
  }

  /**
   * Handle mouse over
   */
  handleMouseEnter (e) {
    let height = e.currentTarget.clientHeight;
    let width = e.currentTarget.clientWidth;
    this.setState({ detail: <Detail left={width / 2} top={height / 2} /> });
  }

  /**
   * Handle mouse leave
   */
  handleMouseLeave (e) {
    this.setState({ detail: null });
  }

  /**
   * Render
   */
  render () {
    return (
      <div
        className='venue-card-container'
        onMouseEnter={this.handleMouseEnter}
        onMouseLeave={this.handleMouseLeave}>
        <div className='venue-info-item'>
          {this.props.data.name}
        </div>
        <div className='venue-img-item'>
          <img src={this.props.data.profile_picture} />
        </div>
        { this.state.detail || '' }
      </div>
    );
  }
}

export default VenueCard;
