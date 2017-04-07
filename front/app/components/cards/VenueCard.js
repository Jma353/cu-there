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
  }

  /**
   * Handle mouse over
   */
  handleMouseEnter (e) {
    let rect = e.currentTarget.getBoundingClientRect();
    let left = (rect.left + rect.right) * 0.5;
    let top = (rect.top + rect.bottom) * 0.5;
    let detail = <Detail owner={this.props.id} left={left} top={top} />;
    this.props.dispatch(actionCreators.didShowDetail(detail));
  }

  /**
   * Render
   */
  render () {
    return (
      <div
        className='venue-card-container'
        onMouseEnter={this.handleMouseEnter} >
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
