import React from 'react';
import Search from '../Search';
import Brand from '../Brand';
require('../../../public/sass/Navigation.scss');

/**
 * Navigation at the top of the application
 */
class Navigation extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='top-nav'>
        <div className='top-bar'>
          <div className='brand-container'>
            <Brand />
          </div>
          <div className='links-container'>
          </div>
        </div>
        <div className='recommend'>
          <div className='briefing md-text'>
            Briefly describe your event
          </div>
          <Search
            submit='Recommend'
            placeholder='e.g. A tech talk hosted by ACSU'
          />
        </div>
      </div>
    );
  }

}

export default Navigation;
