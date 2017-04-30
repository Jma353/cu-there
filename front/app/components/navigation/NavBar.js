import React from 'react';
import Search from '../search/Search';
import { Link } from 'react-router';
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
        <div className='brand-item'>
          <a href='/'>CU There</a>
        </div>
        <div className='search-item'>
          <Search
            initialValue={this.props.query}
            initialCategories={this.props.categories}
            />
        </div>
        <ul className='navbar-links-container'>
          <li className='link-item'><Link to='/about'>About</Link></li>
        </ul>
      </div>
    );
  }
}

export default NavBar;
