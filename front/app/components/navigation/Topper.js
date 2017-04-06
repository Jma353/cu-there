import React from 'react';
import Search from '../Search';
import NavBar from './NavBar';
require('../../../public/sass/Topper.scss');

/**
 * Top of the page
 */
class Topper extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='topper'>
        <NavBar />
        <div className='briefing'>
          Briefly describe your event
          <Search
            submit='Recommend'
            placeholder='e.g. A tech talk hosted by ACSU'
          />
        </div>
      </div>
    );
  }
}

export default Topper;
