import React from 'react';
import Detail from './Detail';
import GoogleMapReact from 'google-map-react';
require('../../../public/sass/VenueDetail.scss');

/**
 * Venue detail view
 */
class VenueDetail extends React.Component {

  /**
   * Render
   */
  render () {
    const Marker = () => { return <div className='map-marker' />; };
    return (
      <Detail {...this.props}>
        <div className='cover-picture'>
          <img src={this.props.data.cover_picture} />
        </div>
        <div className='venue-detail-container'>
          <div className='venue-detail-info'>
            <p className='md-text'>{this.props.data.name}</p>
            <p className='sm-text'>{this.props.data.about}</p>
          </div>
          <div className='venue-detail-visuals'>
            <div className='venue-picture'>
              <img src={this.props.data.profile_picture} />
            </div>
            <div className='venue-map'>
              <GoogleMapReact
                defaultCenter={{
                  lat: this.props.data.location.latitude,
                  lng: this.props.data.location.longitude
                }}
                defaultZoom={11}>
                <Marker
                  lat={this.props.data.location.latitude}
                  lng={this.props.data.location.longitude}
                />
              </GoogleMapReact>
            </div>
          </div>
        </div>
      </Detail>
    );
  }
}

export default VenueDetail;
