import React from 'react';
import { browserHistory } from 'react-router';
require('../../../public/sass/About.scss');

class About extends React.Component {
  render () {
    return (
      <div className='about-container'>
        <button className='back' onClick={() => browserHistory.goBack()}>
          <i className='fa fa-angle-left' aria-hidden='true' /> Back
        </button>
        <h1>About CU There</h1>
        <p>CU There is a class project for CS 4300: Language & Information at Cornell University.</p>
        <p><a href='https://github.com/jma353/cu-there' target='_blank'><i className='fa fa-github' aria-hidden='true' /> GitHub Page</a></p>
        <h3>Authors</h3>
        <ul>
          <li>Annie Cheng</li>
          <li>Joseph Antonakakis</li>
          <li>Amit Mizrahi</li>
          <li>Daniel Li</li>
        </ul>
      </div>
    );
  }
}

export default About;
