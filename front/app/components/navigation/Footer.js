import React from 'react';
require('../../../public/sass/Footer.scss');

/**
 * Footer at the bottom of the application
 */
class Footer extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='footer'>
        <p>(c) Copyright 2017 CU There</p>
      </div>
    );
  }

}

export default Footer;
