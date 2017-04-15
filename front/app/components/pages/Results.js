import React from 'react';
import axios from 'axios';
import NavBar from '../navigation/NavBar';
import TextCardList from '../lists/TextCardList';
import VenueDetail from '../details/VenueDetail';
import Footer from '../navigation/Footer';
require('../../../public/sass/Results.scss');

/**
 * Results page of the application
 */
class Results extends React.Component {

  /**
   * Render
   */
  render () {
    let texts = ['free', 'tech', 'learning', 'memes'];
    let venue = {
      'about': 'Admission is always free! | Twitter & Instagram @HFJMuseum',
      'cover_picture': 'https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/10261_10153836103503817_8408778085864276077_n.jpg?oh=37b98f02ab1b3407cf36e00a637ead68&oe=59610BA6',
      'emails': null,
      'id': '67879373816',
      'location': {
        'city': 'Ithaca',
        'country': 'United States',
        'latitude': 42.45078,
        'longitude': -76.48616,
        'state': 'NY',
        'street': '114 Central Ave',
        'zip': '14853'
      },
      'name': 'Herbert F. Johnson Museum of Art',
      'profile_picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB'
    };
    return (
      <div className='results'>
        <NavBar />
        <TextCardList data={texts} title='Recommended Tags' />
        <VenueDetail data={venue} />
        <Footer />
      </div>
    );
  }

}

export default Results;
