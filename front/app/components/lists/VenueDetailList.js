import React from 'react';
import Map from '../map/Map';
import VenueDetail from '../details/VenueDetail';
require('../../../public/sass/VenueDetailList.scss');

/**
 * Displays information about venues, including geographical mappings
 * of the venues themselves
 */
class VenueDetailList extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.generateDetail = this.generateDetail.bind(this);
  }

  /**
   * Generate a venue detail view
   */
  generateDetail (venue, i) {
    return <VenueDetail data={venue} key={i} />;
  }

  /**
   * Render
   */
  render () {
    let details = this.props.data.map(this.generateDetail);
    let locations = this.props.data.map(d => {
      return {latitude: d.latitude, longitude: d.longitude};
    });
    return (
      <div className='venue-detail-list-container'>
        <div className='venue-detail-list-title'>{this.props.title}</div>
        <div className='venue-detail-list-content'>
          <div className='venue-detail-list-elements'>
            {details}
          </div>
          <div className='venue-detail-list-map'>
            <Map locations={locations} zoom={11} />
          </div>
        </div>
      </div>

    );
  }
}

export default VenueDetailList;
