import React, { Component } from 'react';
import NavBarItem from './NavBarItem';
require('../../../public/sass/NavBar.scss');

/**
 * NavBar at the top of the application
 */
class NavBar extends Component {

  /**
   * Grab list of items
   */
  itemList() {
    return [
      { content: 'a' },
      { content: 'b' },
      { content: 'c' }
    ]
  }

  /**
   * Given `item`, make NavBarItem (`i` is index for key)
   */
  makeItem(item, i) {
    return (<NavBarItem key={i} content={item.content} />)
  }

  /**
   * Render
   */
  render() {
    // Grab several NavBarItems, based on itemList()
    let items = this.itemList().map(this.makeItem);
    return (
      <ul className="menu">
        {items}
      </ul>
    );
  }

}

export default NavBar;
