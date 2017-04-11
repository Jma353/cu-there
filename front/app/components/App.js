import React from 'react';
import axios from 'axios';
import Topper from './navigation/Topper';
import VenueCardList from './lists/VenueCardList';
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
    /*
    let self = this;
    axios.get('/events/venues/')
    .then(resp => {
      self.setState({ venues: resp.data });
    }).catch(err => {
      console.log(err);
    });
    */
  }

  /**
   * Render
   */
  render () {
    let venues = [
    {
    "about": "Through a series of fundamental and unique training methods, Valor is committed to developing you physically, mentally, & emotionally. Live Your Best Life.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/13731586_618083801699047_2351451942195728764_n.jpg?oh=91b0b4bca80bd4374f2bf9fc66ba3f1f&oe=595A1F62",
    "emails": [
    "valorsandc@gmail.com"
    ],
    "id": "232306986943399",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.4723587,
    "longitude": -76.4230728,
    "state": "NY",
    "street": "480 Lower Creek Rd, Ste B",
    "zip": "14850"
    },
    "name": "Valor Strength & Conditioning",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c86.8.180.180/10435920_339824289525001_4696229566211687234_n.png?oh=c097b3372cfac61f0726549d1d89d790&oe=594FFCD1"
    },
    {
    "about": "Admission is always free! | Twitter & Instagram @HFJMuseum",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/10261_10153836103503817_8408778085864276077_n.jpg?oh=37b98f02ab1b3407cf36e00a637ead68&oe=59610BA6",
    "emails": null,
    "id": "67879373816",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.45078,
    "longitude": -76.48616,
    "state": "NY",
    "street": "114 Central Ave",
    "zip": "14853"
    },
    "name": "Herbert F. Johnson Museum of Art",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.200.200/p200x200/64210_10152101770528817_582857435_n.jpg?oh=62c93da872379782c272f66ec6f60c57&oe=59558CAB"
    },
    {
    "about": "Ithaca's own 250 capacity live music saloon venue. 2400 square feet with house stage/sound/backline on the Commons.\nFor booking:  booktherange@gmail.com",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-0/p180x540/17311142_449508158757628_6177551916932944021_o.jpg?oh=1bde40c7cc2c5050b28ab78904a52037&oe=59963B70",
    "emails": [
    "therangeithaca@gmail.com"
    ],
    "id": "272244669817312",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.43943,
    "longitude": -76.49826,
    "state": "NY",
    "street": "119 E. State St",
    "zip": "14850"
    },
    "name": "The Range",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/17155465_440619976313113_4275122384457243958_n.jpg?oh=9048760834ee2c175461fc89efebbc74&oe=596473A3"
    },
    {
    "about": "This page is intended for students and alumni of Risley Residential College for the Creative and Performing Arts at Cornell University. Here you can reconnect with old friends, meet some new friends, and keep up with the awesome happenings in our castle.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-8/s720x720/1149750_186854264829649_695254255_o.jpg?oh=4bc1ef21c9d8f4ddcdde103d934755eb&oe=595522A3",
    "emails": [
    "risley@cornell.edu"
    ],
    "id": "186853051496437",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.453113820089,
    "longitude": -76.481944721314,
    "state": "NY",
    "street": "536 Thurston Ave",
    "zip": "14850"
    },
    "name": "Risley Residential College and Alumni",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c71.65.818.818/s200x200/581996_186853858163023_41881866_n.jpg?oh=dbdc6550e1ff39ba3736e19edd4ee6ed&oe=595C460E"
    },
    {
    "about": "AGAVA is a Southwest-Inspired restaurant, on Ithaca's East Hill ",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-8/s720x720/17097473_1195681270526994_6325010034530129692_o.jpg?oh=7ff3e7cfb43b2b352f6875f0f419f4c2&oe=5994ADC2",
    "emails": [
    "contact@agavarestaurant.com"
    ],
    "id": "176548522440279",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.43829,
    "longitude": -76.4651,
    "state": "NY",
    "street": "381 Pine Tree Rd",
    "zip": "14850"
    },
    "name": "AGAVA",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c15.15.191.191/429993_234881546606976_1403421474_n.jpg?oh=5b3f0d28e05d1355aa83734bce433d5c&oe=5963A3B6"
    },
    {
    "about": "The Downtown Ithaca Alliance welcomes you to Downtown Ithaca where you can shop, dine, work, and play. It's yours to discover!",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/525642_10151443551575576_327375669_n.jpg?oh=eb00b4463dceac7fa0188364a551bcc0&oe=5998751B",
    "emails": [
    "info@downtownithaca.com"
    ],
    "id": "132710300575",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.440091482849,
    "longitude": -76.496230856002,
    "state": "NY",
    "zip": "14850"
    },
    "name": "Downtown Ithaca",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c39.37.467.467/s200x200/392900_10152696293625576_1390924941_n.jpg?oh=32fac844eedf16c0a77d9a77b5dae4fb&oe=596225F6"
    },
    {
    "about": "FGSS studies a wide range of fields from the perspectives of feminist and LGBTQIA critical analysis in global and local contexts to promote social justice.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-8/s720x720/16463319_1876416505936887_7999759779290496182_o.png?oh=8cf39b16be7c32d3273e815cf3e45dec&oe=59985340",
    "emails": [
    "fgss@cornell.edu"
    ],
    "id": "1875442059367665",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.44923017953,
    "longitude": -76.481612920761,
    "state": "NY",
    "street": "231 East Ave",
    "zip": "14853"
    },
    "name": "Feminist, Gender, and Sexuality Studies",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/16427361_1875443586034179_6605809417160889465_n.jpg?oh=861993c1224dae5cf163024e425223cf&oe=59976D23"
    },
    {
    "about": "Monks On The Commons- Modern American Food offering Soulful food & Sinful Cocktails.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/15697575_357810567929286_6095258740853881897_n.jpg?oh=95e35e5ac4bc19cd3ef4b3643df9fa72&oe=59653B60",
    "emails": [
    "matthew.wilde@marriott.com"
    ],
    "id": "329079997469010",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.438724,
    "longitude": -76.4953472,
    "state": "NY",
    "street": "120 South Aurora St",
    "zip": "14850"
    },
    "name": "Monks On The Commons",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/17098408_389112708132405_7177704122369613532_n.jpg?oh=9358ede0faf6479f108bd21012dbbd9a&oe=5954B445"
    },
    {
    "about": "Cornell Fitness Centers offer safe, convenient, effective, and enjoyable exercise opportunities with five fitness centers located around campus.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/10689868_868062976562798_6864496672880207429_n.jpg?oh=56d628b0c72e1f94c51c61d2d515bc4d&oe=59632248",
    "emails": [
    "fitness@cornell.edu"
    ],
    "id": "862552723780490",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.4531151,
    "longitude": -76.4780588,
    "state": "NY",
    "street": "Helen Newman Hall; 163 Cradit Farm Dr",
    "zip": "14853"
    },
    "name": "Big Red Rec",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/10857833_866936446675451_2058107884045277454_n.png?oh=e8ed350ea0aeeba7c82e268a8d9c33c0&oe=595586D1"
    },
    {
    "about": "\"Showcasing Hospitality Education Through Student Leadership\"\n\nThe 92nd Annual Hotel Ezra Cornell\nMarch 16-19th, 2017\nCornell University, Ithaca, NY",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/16602655_10158109285905577_9070452768264648870_n.png?oh=5348d0552001bbde3c836d17896dd7b2&oe=5963D221",
    "emails": [
    "hec@cornell.edu"
    ],
    "id": "261083115576",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.4458,
    "longitude": -76.4816,
    "state": "NY",
    "street": "G75 Statler Hall",
    "zip": "14853"
    },
    "name": "Hotel Ezra Cornell",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/1560694_10155520112070577_1991277561861458586_n.jpg?oh=7fba23e2d2a70395dbc836b372be7847&oe=5992DEA0"
    },
    {
    "about": "Cornell University is an Ivy League university located in Ithaca, New York, USA",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-0/p480x480/17635348_10155026704840132_4413449940353972931_o.jpg?oh=753e672708d6c0d7ba0f6e8d0ef28cc2&oe=594FC205",
    "emails": [
    "socialmedia@cornell.edu"
    ],
    "id": "8570160131",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.445907071396,
    "longitude": -76.482094292009,
    "state": "NY",
    "zip": "14853"
    },
    "name": "Cornell University",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/484745_10151989689985132_1461524573_n.png?oh=90c8dfd9d5dbe0e4332fee703e23a092&oe=59506C2B"
    },
    {
    "about": "High-quality, unique and delicious food and beverages. This page is your official source for CTB information.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-8/s720x720/17390559_10155022621596000_3880277082361240465_o.jpg?oh=ecbd5088070cde9ed32caf6a2801f3e4&oe=5967A46C",
    "emails": [
    "travis@collegetownbagels.com"
    ],
    "id": "113060610999",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.442698687526,
    "longitude": -76.484906673431,
    "state": "NY",
    "street": "415 College Avenue",
    "zip": "14850"
    },
    "name": "Collegetown Bagels",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/12742642_10153914872621000_9110450767965274553_n.jpg?oh=4a2a855b210714523e3c035b4e1ae2d6&oe=59635A65"
    },
    {
    "about": "Cornell Cinema has been cited as one of the best campus film exhibition programs in the country, screening close to 150 different films/videos each year, five nights a week in the beautiful Willard Straight Theatre.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/17634849_10158620433520529_3336516412665958022_n.png?oh=c6f3e070e585cde2d484fde9f28a9c1d&oe=59502445",
    "emails": null,
    "id": "215249100528",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.4458606,
    "longitude": -76.4860489,
    "state": "NY",
    "street": "104 Willard Straight Hall",
    "zip": "14850"
    },
    "name": "Cornell Cinema",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/c24.0.200.200/p200x200/1175506_10153160570160529_509717013_n.jpg?oh=44ab5d49a650be63ad079b10cf2c0951&oe=595B4C39"
    },
    {
    "about": "Loco Cantina is your local bar and grill specializing in Margaritas! A relaxed atmosphere with casual table service and lively nights. ",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/13178662_1039640809454083_7919432980467223947_n.jpg?oh=26f2e7305ff17b793da4a9bf2cdee930&oe=59544870",
    "emails": [
    "info.lococantina@gmail.com"
    ],
    "id": "107002662717907",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.44203,
    "longitude": -76.48997,
    "state": "NY",
    "street": "308-310 Stewart Ave",
    "zip": "14850"
    },
    "name": "Loco Cantina",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/14051_823731924378307_3264406997966184972_n.jpg?oh=5cfbf160426e6c012e18e98f5084aa02&oe=59911EE2"
    },
    {
    "about": "Northstar is proud to present Casita Del Polaris! Event/music/entertainment space for us all to enjoy the nice nice vibes. ",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/11047910_1393560954303089_4416249134979091721_n.jpg?oh=8a0f32f99b4588560c96b5173aa8043f&oe=595B4DE9",
    "emails": [
    "castia@northstarpub.com"
    ],
    "id": "1392746251051226",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.4533195,
    "longitude": -76.4975281,
    "state": "NY",
    "street": "1201 N Tioga St Unit 2",
    "zip": "14850"
    },
    "name": "Casita Del Polaris",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/11181806_1392749734384211_3456876949970518720_n.jpg?oh=4a985deba8dc7804ffac6a0a9d8c1dbd&oe=595D041A"
    },
    {
    "about": "Welcome to the Ithaca Ale House. Located in the heart of restaurant row on Aurora Street, we offer a unique and exciting dining experience. Choose from our extensive, ever changing 20 tap craft beer selection with brews from all over the country.",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/1375149_10152045211628969_1640008262_n.png?oh=f72d1b0e8adf97e9fad51f24be38b348&oe=595DC1C6",
    "emails": null,
    "id": "283098828968",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.439973849624,
    "longitude": -76.495663403693,
    "state": "NY",
    "street": "111 N Aurora St",
    "zip": "14850"
    },
    "name": "The Ithaca Ale House",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/1383397_10152041063853969_1885351189_n.jpg?oh=096ef8aee4996b0b9d57da33b19f4536&oe=595351BB"
    },
    {
    "about": "The official Cornell University store, celebrating everything Cornell & helping you succeed.  store.cornell.edu",
    "cover_picture": "https://scontent.xx.fbcdn.net/v/t31.0-8/s720x720/17621837_1359273220762267_6482924337646126574_o.jpg?oh=6cd79bde53ec7ea8f415a650c2b2fd98&oe=5959E1F5",
    "emails": [
    "store@cornell.edu"
    ],
    "id": "273574049332195",
    "location": {
    "city": "Ithaca",
    "country": "United States",
    "latitude": 42.446805736861,
    "longitude": -76.484309346109,
    "state": "NY",
    "street": "135 Ho Plz",
    "zip": "14853"
    },
    "name": "The Cornell Store",
    "profile_picture": "https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/321649_276900412332892_232720925_n.jpg?oh=1e01c56eec89cfa9bc259898643e1d6f&oe=595267C6"
    }
    ]

    return (
      <div>
        <Topper />
        <VenueCardList venues={venues} title='Popular Venues' />
        <Footer />
      </div>
    );
  }
}

export default App;
