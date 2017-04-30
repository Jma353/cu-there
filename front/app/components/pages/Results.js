import React from 'react';
import NavBar from '../navigation/NavBar';
import TextCardList from '../lists/TextCardList';
import VenueDetailList from '../lists/VenueDetailList';
import EventDetailList from '../lists/EventDetailList';
import Footer from '../navigation/Footer';
import TimeGraph from '../graphs/TimeGraph';
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
    this.props.dispatch(
      actionCreators.didSearch(
        this.props.location.query.q,
        this.props.location.query.categs
      )
    );
  }

  /**
   * Format time to 12 hour system
   */
  formatTime (times) {
    var formattedTimes = [];

    times = times.map(function(e) {
      return e.split(":");
    });

    // Sort times array
    times = times.sort(function (a, b) {
      if (a[0] < b[0]) { // Earlier hour
        return -1;
      } else if (a[0] > b[0]) { // Later hour
        return 1;
      }

      // Same hour, so compare minutes
      if (a[1] < b[1]) { // Earlier minutes
        return -1;
      } else if (a[1] > b[1]) { // Later minutes
        return 1;
      }

      return 0;
    });

    for (var i = 0; i < times.length; i++) {
      var hour = times[i][0];
      var min = times[i][1];
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
            {times.length && response.timeGraphs.length &&
              <div className='result-times'>
                <TextCardList data={this.formatTime(times)} title='Suggested Times' />
                <TimeGraph data={response.timeGraphs} />
              </div>
            }
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
