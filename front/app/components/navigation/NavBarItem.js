import React, { Component } from 'react';

/**
 * An item of the NavBar
 */
class NavBarItem extends Component {

  /**
   * Render
   */
  render() {
    let content = this.props.content;
    return (
      <li>{content}</li>
    );
  }

}

export default NavBarItem;
