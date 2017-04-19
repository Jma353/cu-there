import React from 'react';
import axios from 'axios';
import Topper from '../navigation/Topper';
import VenueCardList from '../lists/VenueCardList';
import Footer from '../navigation/Footer';
require('../../../public/sass/Home.scss');

/**
 * Home page of the application
 */
class Home extends React.Component {

  /**
   * Constructor - initializes state
   */
  constructor (props) {
    super(props);
    this.state = { venues: [] };
  }

  /**
   * When component mounts, make various IR requests
   */
  componentDidMount () {
    console.log('Is this getting called even');
    axios.get('/venues')
    .then(resp => {
      console.log(resp);
      this.setState({ venues: resp.data.venues });
    })
    .catch(err => {
      console.log(err);
    });
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='home'>
        <Topper />
        <VenueCardList
          data={this.state.venues}
          title='Popular Venues' />
        <Footer />
      </div>
    );
  }

}

export default Home;
