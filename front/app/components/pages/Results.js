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
   * Format time to 12 hour system
   */
  formatTime (times) {
    var formattedTimes = [];

    for (var i = 0; i < times.length; i++) {
      var timeComps = times[i].split(":");
      var hour = timeComps[0];
      var min = timeComps[1];
      var ampm = (hour >= 12) ? 'PM' : 'AM';
      hour = hour % 12;
      hour = hour ? hour : 12;
      var time = hour + ':' + min + ' ' + ampm;

      if (!formattedTimes.includes(time)) {
        formattedTimes.push(time);
      }
    }

    return (formattedTimes);
  }

  /**
   * Render
   */
  render () {
    const response = this.props.results.response;
    const categories = this.props.location.query.categs;
    // Quick time formatting
    const times = response.times.map((time, i) => {
      return time + ':00';
    }).filter((time) => {
      return time !== '1:00';
    });

    return (
      <div>
        <NavBar
          query={this.props.location.query.q}
          categories={categories && categories.split(',')}
          />
        <div className='results-header'>
          <p>{`Showing ${Object.keys(response.venues).length} venues`}</p>
        </div>
        <div className='results'>
          <div className='result-text-card-lists'>
            {/*
            <div className='result-tags'>
              <TextCardList data={response.tags} title='Tags' />
            </div>
            */}
            {times.length !== 0 ? <div className='result-times'>
              <TextCardList data={this.formatTime(times)} title='Suggested Times' />
            </div> : null}
          </div>
          <VenueDetailList data={response.venues} title='Venues' />
          <EventDetailList data={this.props.results.events.all} title='Related Events' />
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
