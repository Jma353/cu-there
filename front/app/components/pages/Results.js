import React from 'react';
import axios from 'axios';
import NavBar from '../navigation/NavBar';
import TextCardList from '../lists/TextCardList';
import VenueDetailList from '../lists/VenueDetailList';
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
    let tags = ['free', 'tech', 'learning', 'memes', 'gates', 'internship', 'jobs', 'microsoft', 'coding', 'challenge'];
    let times = ['Thurs 11:00AM', 'Fri 7:00PM', 'Mon 6:30PM', 'Wed 12:00PM', 'Tues 9:00AM'];
    let venues = [
      {
        'about': 'Through a series of fundamental and unique training methods, Valor is committed to developing you physically, mentally, & emotionally. Live Your Best Life.',
        'cover_picture': 'https://scontent.xx.fbcdn.net/v/t1.0-9/13731586_618083801699047_2351451942195728764_n.jpg?oh=91b0b4bca80bd4374f2bf9fc66ba3f1f&oe=595A1F62',
        'emails': [
          'valorsandc@gmail.com'
        ],
        'id': '232306986943399',
        'location': {
          'city': 'Ithaca',
          'country': 'United States',
          'latitude': 42.4723587,
          'longitude': -76.4230728,
          'state': 'NY',
          'street': '480 Lower Creek Rd, Ste B',
          'zip': '14850'
        },
        'name': 'Valor Strength & Conditioning',
        'profile_picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/c86.8.180.180/10435920_339824289525001_4696229566211687234_n.png?oh=c097b3372cfac61f0726549d1d89d790&oe=594FFCD1'
      },
      {
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
      },
      {
        'about': 'Ithaca\'s own 250 capacity live music saloon venue. 2400 square feet with house stage/sound/backline on the Commons.\nFor booking:  booktherange@gmail.com',
        'cover_picture': 'https://scontent.xx.fbcdn.net/v/t31.0-0/p180x540/17311142_449508158757628_6177551916932944021_o.jpg?oh=1bde40c7cc2c5050b28ab78904a52037&oe=59963B70',
        'emails': [
          'therangeithaca@gmail.com'
        ],
        'id': '272244669817312',
        'location': {
          'city': 'Ithaca',
          'country': 'United States',
          'latitude': 42.43943,
          'longitude': -76.49826,
          'state': 'NY',
          'street': '119 E. State St',
          'zip': '14850'
        },
        'name': 'The Range',
        'profile_picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/17155465_440619976313113_4275122384457243958_n.jpg?oh=9048760834ee2c175461fc89efebbc74&oe=596473A3'
      }
    ];
    return (
      <div>
        <NavBar />
        <div className='results'>
          <div className='result-text-card-lists'>
            <div className='result-tags'>
              <TextCardList data={tags} title='Tags' />
            </div>
            <div className='result-times'>
              <TextCardList data={times} title='Times' />
            </div>
          </div>
          <VenueDetailList data={venues} title='Venues' />
        </div>
        <Footer />
      </div>
    );
  }

}

export default Results;
