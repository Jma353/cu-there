import React from 'react';
import Topper from './navigation/Topper';
import VenueList from './lists/VenueList';
import Footer from './navigation/Footer';
require('../../public/sass/App.scss');

/* Redux */
import { connect } from 'react-redux';

/**
 * Main application component.
 */
class App extends React.Component {

  /**
   * Render
   */
  render () {
    // Test venues
    let venues = [
      { name: 'First Title', 'profile_picture': 'https://goo.gl/vy9h8P' },
      { name: 'Hello World', profile_picture: 'https://goo.gl/vy9h8P' },
      { name: 'Varying Sized Cards', profile_picture: 'https://goo.gl/vy9h8P' },
      { name: 'Herbert F. Johnson Museum of Art', profile_picture: 'https://goo.gl/vy9h8P' },
      { name: 'Herbert F. Johnson Museum of Art Plus Long Title Extension', profile_picture: 'https://goo.gl/vy9h8P' }
    ];
    return (
      <div>
        <Topper />
        <VenueList venues={venues} setDetail={this.setDetail} />
        <Footer />
        { this.props.detail || '' }
      </div>
    );
  }

}

/* Redux connection */
let mapStateToProps = (state, props) => {
  return { ...props, detail: state._detail.detail };
};

export default connect(mapStateToProps)(App);
