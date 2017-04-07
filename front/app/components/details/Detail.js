import React from 'react';
require('../../../public/sass/Detail.scss');

/* Redux */
import { connect } from 'react-redux';

/**
 * Reusable detail view (events, venues, etc.)
 */
class Detail extends React.Component {

  /**
   * Render
   */
  render () {
    let position = {
      left: this.props.left,
      top: this.props.top
    };
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

const ConnectedDetail = connect()(Detail);
export default ConnectedDetail;
