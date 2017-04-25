import React from 'react';
require('../../../public/sass/MapMarker.scss');

class MapMarker extends React.Component {

  /**
   * Render
   */
  render () {
    let places = this.props.data.map(d => { return d.name; }).join(' | ');
    return (
      <div className='map-marker'>
        <span className='map-marker-tool-tip'>
          {places}
        </span>
      </div>
    );
  }
}

export default MapMarker;
