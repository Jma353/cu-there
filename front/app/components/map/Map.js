import React from 'react';
import GoogleMapReact from 'google-map-react';
import MapMarker from '../map/MapMarker';
require('../../../public/sass/Map.scss');

class Map extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.mean = this.mean.bind(this);
    this.generateMapMarker = this.generateMapMarker.bind(this);
  }

  /**
   * Mean calculation
   */
  mean (arr) {
    let tot = 0;
    for (let i = 0; i < arr.length; i++) tot += arr[i];
    return tot / arr.length;
  }

  /**
   * Generate a map marker
   */
  generateMapMarker (location) {
    return <MapMarker
      lat={location.latitude}
      lng={location.longitude}
      key={location.latitude + ':' + location.longitude} />;
  }

  /**
   * Render
   */
  render () {
    let center = {
      lat: this.mean(this.props.locations.map(l => { return l.latitude; })),
      lng: this.mean(this.props.locations.map(l => { return l.longitude; }))
    };
    let markers = this.props.locations.map(this.generateMapMarker);
    markers = markers.filter(l => {
      return !isNaN(l.lat) && !isNaN(l.lng);
    });
    return (
      <div className='map'>
        <GoogleMapReact
          defaultCenter={center}
          defaultZoom={this.props.zoom}>
          {markers}
        </GoogleMapReact>
      </div>
    );
  }
}

export default Map;
