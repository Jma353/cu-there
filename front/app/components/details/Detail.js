import React from 'react';
require('../../../public/sass/Detail.scss');

/**
 * Reusable detail view (events, venues, etc.)
 */
class Detail extends React.Component {

  /**
   * Render
   */
  render () {
    // All positioning info
    let detailStyle = { top: this.props.y };
    let pointerStyle = { left: this.props.x };
    return (
      <div className='detail' style={detailStyle}>
        <div className='detail-pointer' style={pointerStyle} />
        <div className='detail-contents-container'>
          {this.props.contents}
        </div>
      </div>
    );
  }

}

export default Detail;
