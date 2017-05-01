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
        <div className='brand-item'>=
          <Link to='/'>CU There</Link>
        </div>
        <div className='search-item'>
          <Search
            initialValue={this.props.query}
            initialCategories={this.props.categories}
            initialRelatedWords={this.props.initialRelatedWords}
            relatedWords={this.props.relatedWords}
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
