import React from 'react';

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
    this.generateMapMarker = this.generateMapMarker.bind(this);
  }

  /**
   * Generate a venue detail view
   */
  generateDetail (venue) {
    // TODO
  }

  /**
   * Generate a map marker
   */
  generateMapMarker (venue) {
    // TODO
  }

  /**
   * Render
   */
  render () {
    let details = this.props.data.map(this.generateDetail);
    let markers = this.props.data.map(d => { return this.generateMapMarker(d.location); });
    // TODO
    return (
      <div />
    );
  }
}

export default VenueDetailList;
