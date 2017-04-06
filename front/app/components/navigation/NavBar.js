import React from 'react';
require('../../../public/sass/NavBar.scss');

/**
 * Reusable navbar at the top of the application
 */
class NavBar extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='navbar-container'>
        <div className='brand-item'><a href='/'>CU There</a></div>
        <ul className='navbar-links-container'>
          <li className='link-item'><a href='/about'>About</a></li>
        </ul>
      </div>
    );
  }
}

export default NavBar;
