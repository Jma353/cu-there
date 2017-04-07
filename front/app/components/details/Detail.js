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
    let position = { left: this.props.left, top: this.props.top };
    return (
      <div
        className='detail'
        style={position} >
        <div className='top-line' />
        <div className='detail-contents-container'>
          {this.props.contents}
        </div>
      </div>
    );
  }
}

export default Detail;
