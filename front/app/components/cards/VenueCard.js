import React from 'react';
import VenueDetail from '../details/VenueDetail';
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
    let detail = <VenueDetail
      left={width / 2}
      top={height / 2}
      data={this.props.data} />;
    this.setState({ detail: detail });
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
          <p>{this.props.data.location.city + ', ' + this.props.data.location.state }</p>
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
