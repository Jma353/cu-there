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
    console.log(location);
    return <MapMarker
      lat={location.latitude}
      lng={location.longitude}
      key={location.latitude + ':' + location.longitude}
      data={location.venues} />;
  }

  /**
   * Render
   */
  render () {
    let center = {
      lat: this.mean(this.props.locations.map(l => { return l.latitude; })) || 42.447605,
      lng: this.mean(this.props.locations.map(l => { return l.longitude; })) || -76.484878
    };

    // Results -> cluster events by location
    let results = {};
    for (let i = 0; i < this.props.locations.length; i++) {
      let l = this.props.locations[i];
      let k = l.latitude + ':' + l.longitude;
      if (results[k]) {
        results[k].venues.push(l.data);
      } else {
        results[k] = {};
        results[k].latitude = l.latitude;
        results[k].longitude = l.longitude;
        results[k].venues = [];
        results[k].venues.push(l.data);
      }
    }

    // Convert to array
    let locales = [];
    for (let k in results) {
      locales.push(results[k]);
    }

    let markers = locales.map(this.generateMapMarker);
    return (
      <div className='map'>
        <GoogleMapReact
          bootstrapURLKeys={{ key: 'AIzaSyBhHhJf3TxNZLxwSci5VjLST3fjNJaGUD8' }}
          defaultCenter={center}
          defaultZoom={this.props.zoom}>
          {markers}
        </GoogleMapReact>
      </div>
    );
  }
}

export default Map;
