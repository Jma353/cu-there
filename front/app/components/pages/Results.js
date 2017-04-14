import React from 'react';
import axios from 'axios';
import NavBar from '../navigation/NavBar';
import Footer from '../navigation/Footer';
require('../../../public/sass/Results.scss');

/**
 * Results page of the application
 */
class Results extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='results'>
        <NavBar />
        <Footer />
      </div>
    );
  }

}

export default Results;
