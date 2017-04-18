import React from 'react';
import NavBar from '../navigation/NavBar';
import TextCardList from '../lists/TextCardList';
import VenueDetailList from '../lists/VenueDetailList';
import EventDetailList from '../lists/EventDetailList';
import Footer from '../navigation/Footer';
require('../../../public/sass/Results.scss');

/* Redux */
import { connect } from 'react-redux';
import * as actionCreators from '../redux/actionCreators';

/**
 * Results page of the application
 */
class Results extends React.Component {

  /**
   * When the component mounts, do stuff
   */
  componentDidMount () {
    this.props.dispatch(actionCreators.didSearch(this.props.location.query.q));
  }

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
    let events = [
      {
        "description": "Come out to a virtual session with Squarespace product designer Danni Fisher! Learn about the Design team at Squarespace, what makes a \"good\" design portfolio, the product development cycle,  how design collaborates with engineering, and Q&A.\n\nAnyone with interest in design/engineering is welcome!\n\nP.S. There will be Squarespace swag and food provided for attendees. :)",
        "end_time": "2017-03-27T18:30:00-0400",
        "name": "Squarespace Design Session",
        "place": {
          "name": "Gates G01"
        },
        "start_time": "2017-03-27T17:30:00-0400",
        "id": "1225606194202189",
        "rsvp_status": "attending"
      },
      {
        "description": "not a hackathon\n\nREPEAT. NOT A HACKATHON.\n\ncome get shwifty with some of your coolest CS buddies in a venue that's not Gates\n\nhttps://s-media-cache-ak0.pinimg.com/736x/a6/cc/30/a6cc30bbe524537d9763636f9cacc638.jpg",
        "name": "CS Party",
        "place": {
          "name": "131 N Quarry St"
        },
        "start_time": "2016-11-12T22:00:00-0500",
        "id": "531920573677056",
        "rsvp_status": "attending"
      },
      {
        "description": "The McGraw Clocktower. Cornell's most famous erection has stood at attention atop Libe Slope for generations. Now, something terrible has happened, and the Clocktower is believed to be dead and gone. Authorities have tracked the culprit down to the Men of Last Call All-Male a Cappella group. But of course! One Callboy, Colton Haney '17, has always felt upstaged by the enormous tower! Yet, Colton denies any wrongdoing, and some believe his accusers may have mistook him as any one of the other fifteen devilishly handsome Callboys. Everyone is a suspect. To get to the bottom of this nefarious act and see it all played out live, be at Statler Auditorium on Saturday, November 5th at 8pm.\n\nTalk to any suspect for tickets to the main event, or visit www.menoflastcall.com to order online. Get those tickets while they're still available!\nFor more, check out our online content!\nFacebook: The Men of Last Call\nTwitter, Insta, Snapchat: menoflastcall",
        "end_time": "2016-11-05T21:30:00-0400",
        "name": "Last Call - Save the Clocktower XXI: Who Killed the Clocktower?",
        "place": {
          "name": "Statler Auditorium",
          "location": {
            "city": "Ithaca",
            "country": "United States",
            "latitude": 42.445488757135,
            "located_in": "305683741868",
            "longitude": -76.482200056817,
            "state": "NY",
            "zip": "14853"
          },
          "id": "207854055902890"
        },
        "start_time": "2016-11-05T20:00:00-0400",
        "id": "1027906797338740",
        "rsvp_status": "attending"
      },
      {
        "description": "Dan Smalls Presents Regina Spektor at the State Theatre of Ithaca on 10/14!\n\n7:00PM Doors\n8:00PM Show\n\nRegina Spektor\nMoscow-born alternative singer/songwriter who began in New York's anti-folk scene before making her commercial breakthrough in 2004. All Ages.",
        "end_time": "2016-10-14T23:00:00-0400",
        "name": "Regina Spektor",
        "place": {
          "name": "State Theatre of Ithaca",
          "location": {
            "city": "Ithaca",
            "country": "United States",
            "latitude": 42.439299287036,
            "longitude": -76.499444786181,
            "state": "NY",
            "street": "107 W State St",
            "zip": "14850"
          },
          "id": "11128345140"
        },
        "start_time": "2016-10-14T20:00:00-0400",
        "id": "1752017265087065",
        "rsvp_status": "unsure"
      }
    ];
    return (
      <div>
        <NavBar query={this.props.location.query.q} />
        <div className='results-header'>
          <p>Showing 42 results</p>
        </div>
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
          <EventDetailList data={events} title='Related Events' />
        </div>
        <Footer />
      </div>
    );
  }

}

/** Map the redux state to this component's props */
const mapStateToProps = (state) => {
  return {
    results: state._search.results
  };
};

export default connect(mapStateToProps)(Results);
