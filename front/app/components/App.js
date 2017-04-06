import React from 'react';
import Topper from './navigation/Topper';
import VenueList from './lists/VenueList';
import Footer from './navigation/Footer';
require('../../public/sass/App.scss');

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
      {
        name: 'First Title',
        profile_picture: 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
      },
      {
        name: 'Hello World',
        profile_picture: 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
      },
      {
        name: 'Varying Sized Cards',
        profile_picture: 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
      },
      {
        name: 'Herbert F. Johnson Museum of Art',
        profile_picture: 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
      },
      {
        name: 'Herbert F. Johnson Museum of Art Plus Long Title Extension',
        profile_picture: 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
      }
    ];
    return (
      <div>
        <Topper />
        <VenueList venues={venues} />
        <Footer />
      </div>
    );
  }

}

export default App;
