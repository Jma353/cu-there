import React from 'react';
import Search from '../search/Search';
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
        <div className='filter'>
          <ul className='topper-links'>
            <li className='topper-link-item'><a href='/about'>About</a></li>
          </ul>
          <div className='title'>CU There</div>
          <div className='briefing'>
            Plan your next event at Cornell.
          </div>
          <div className='topper-search'>
            <Search light />
          </div>
        </div>
      </div>
    );
  }
}

export default Topper;
