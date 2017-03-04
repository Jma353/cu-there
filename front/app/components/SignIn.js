import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';
import axios from 'axios';

/**
 * Sign In Component (Google, Facebook in the future)
 */
class SignIn extends Component {

  /* On Google Sign-In Success */
  onGoogleSuccess (r1) {
    // Configuration for POST to backend -> Google
    var config = { headers: {'X-Requested-With': 'XMLHttpRequest'} }
    // Make that POST + print results
    axios.post('/accounts/sign_in', r1, config)
    .then((r2) => {
      console.log(r2);
    });
  }

  /* On Google Sign-In Failure */
  onGoogleFailure (response) {
    console.log(response);
  }

  /* Render */
  render () {
    const customStyle = {
      display: 'inline-block',
      background: '#d14836',
      color: '#fff',
      width: 190,
      paddingTop: 10,
      paddingBottom: 10,
      borderRadius: 2,
      border: '1px solid transparent',
      fontSize: 16,
      fontWeight: 'bold'
    }

    return (
      <GoogleLogin
        clientId="366654572460-sdnq9onsk1ncei8emper3jaamekb45o7.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={this.onGoogleSuccess.bind(this)}
        onFailure={this.onGoogleFailure.bind(this)}
        style={customStyle}
        offline={true}
      />
    )
  }

}

export default SignIn;
