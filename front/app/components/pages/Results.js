import React from 'react';
import axios from 'axios';
import NavBar from '../navigation/NavBar';
import TextCard from '../cards/TextCard';
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
        <TextCard data='yolo-swag' />
        <Footer />
      </div>
    );
  }

}

export default Results;
