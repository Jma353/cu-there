import React from 'react';
require('../../public/sass/Brand.scss');

class Brand extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className={'brand md-text ' + this.props.className}>
        <a href='/'>
          CU There
        </a>
      </div>
    );
  }
}

export default Brand;
