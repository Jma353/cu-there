import React, { Component } from 'react'
import {
  Well,
  Row,
  Col
} from 'React-Bootstrap'
require('../../../public/sass/Footer.scss')

/**
 * Footer at the bottom of the application
 */
class Footer extends Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='footer'>
        <Col xs={6} className='text-center footer-link'>
          <a href='/first' className='footer-link'>First Footer Link</a>
        </Col>
        <Col xs={6} className='text-center footer-link'>
          <a href='/second' className='footer-link'>Second Footer Link</a>
        </Col>
        <Col xs={6} className='text-center footer-link'>
          <a href='/third'>Third Footer Link</a>
        </Col>
        <Col xs={6} className='text-center footer-link'>
          <a href='/fourth'>Fourth Footer Link</a>
        </Col>
      </div>
    )
  }

}

export default Footer
