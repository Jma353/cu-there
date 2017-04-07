import React from 'react';
import axios from 'axios';
import Topper from './navigation/Topper';
import VenueList from './lists/VenueList';
import Footer from './navigation/Footer';
require('../../public/sass/App.scss');

/**
 * Main application component.
 */
class App extends React.Component {

  constructor (props) {
    super(props);
    this.state = { venues: [] };
  }

  componentDidMount () {
    let self = this;
    axios.get('/events/venues/')
    .then(resp => {
      self.setState({ venues: resp.data });
    }).catch(err => {
      console.log(err);
    });
  }

  /**
   * Render
   */
  render () {
    return (
      <div>
        <Topper />
        <VenueList venues={this.state.venues} />
        <Footer />
      </div>
    );
  }
}

export default App;
