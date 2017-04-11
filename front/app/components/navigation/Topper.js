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
            Help us help you plan your next event at Cornell.
          </div>
          <div className='topper-search'>
            <Search
              submit='Recommend'
              placeholder='e.g. A tech talk hosted by ACSU'
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Topper;
