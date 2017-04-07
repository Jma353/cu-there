import React from 'react';
import Detail from '../details/Detail';
require('../../../public/sass/VenueCard.scss');

/* Redux */
import * as actionCreators from '../redux/ActionCreators';
import { connect } from 'react-redux';

/**
 * A card to display basic info about a venue
 */
class VenueCard extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.handleMouseEnter = this.handleMouseEnter.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
  }

  /**
   * Handle mouse over
   */
  handleMouseEnter (e) {
    let rect = e.currentTarget.getBoundingClientRect();
    let left = (rect.left + rect.right) * 0.5;
    let top = window.pageYOffset + (rect.top + rect.bottom) * 0.5;
    let detail = <Detail left={left} top={top} />;
    this.props.dispatch(actionCreators.didShowDetail(detail));
  }

  /**
   * Handle mouse leave
   */
  handleMouseLeave (e) {
    this.props.dispatch(actionCreators.didHideDetail());
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
      </div>
    );
  }
}

const ConnectedVenueCard = connect()(VenueCard);
export default ConnectedVenueCard;
