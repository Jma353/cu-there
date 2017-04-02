import React, { Component } from 'react'
import {
  Nav,
  Navbar,
  NavItem
} from 'React-Bootstrap'
require('../../../public/sass/Navigation.scss')

/**
 * Navigation at the top of the application
 */
class Navigation extends Component {

  /**
   * Render
   */
  render () {
    return (
      <Navbar collapseOnSelect>
        <Navbar.Header>
          <Navbar.Brand>
            <a href='/'>CU There</a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav pullRight>
            <NavItem eventKey={1} href='/about'>About</NavItem>
            <NavItem eventKey={2} href='/venues'>Venues</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    )
  }

}

export default Navigation
