import React from 'react';
require('../../../public/sass/EventDetail.scss');

/* Redux */
import { connect } from 'react-redux';
import * as actionCreators from '../redux/actionCreators';

/**
 * Presents event information / allows the user
 * to reject or accept events accordingly
 */
class EventDetail extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  /**
   * Handle click
   */
  handleClick (e) {
    // All events
    let all = this.props.allEvents;

    // Relevant / irrelevant listingss
    let relevant = this.props.relevant;
    let irrelevant = this.props.irrelevant;

    // Remove this event from relevant + add it to irrelevant
    relevant.splice(relevant.indexOf(this.props.data.id), 1);
    irrelevant.push(this.props.data.id);

    // Remove this event in general
    let ids = all.map(a => { return a.id; });
    let i = ids.indexOf(this.props.data.id);
    all.splice(i, 1);

    // Dispatch this event b/c relevance changed
    this.props.dispatch(
      actionCreators.didChangeRelevance(
        this.props.currentQuery,
        this.props.categories,
        relevant,
        irrelevant,
        all,
        this.props.location.query.related_words
      )
    );
  }

  /**
   * Format datetime
   */
  formatDateTime (d) {
    if (!d) return null; // Date is null

    var date = new Date(d);
    var hours = date.getHours();
    var mins = date.getMinutes();
    var ampm = (hours >= 12) ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours || 12;
    mins = (mins < 10) ? '0' + mins : mins;
    var time = hours + ':' + mins + ' ' + ampm;

    var monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];

    return ([monthNames[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear(), time]);
  }

  /**
   * Format event time given start and end time
   */
  formatEventTime (startDate, endDate) {
    var start = this.formatDateTime(startDate);
    var end = this.formatDateTime(endDate);
    var eventTime = '';

    if (start && end) { // Start and end datetime exist
      if (start[0] === end[0]) { // Same start and end date
        eventTime = start.join(' at ') + ' - ' + end[1];
      } else {
        eventTime = start.join(' at ') + ' - ' + end.join(' at ');
      }
    } else if (!start && !end) { // Start and end datetime don't exist
      eventTime = 'TBD';
    } else if (start) { // Only start datetime exists
      eventTime = start.join(' at ');
    } else { // Only end datetime exists
      eventTime = end.join(' at ');
    }

    return eventTime;
  }

  /**
   * Set text to 'None' if empty
   */
  setDefaultText (text) {
    return text || 'None';
  }

  /**
   * Generate event description string with similar words marked
   */
  markSimilarWords (eventDesc, simWords) {
    simWords.map(function (word) {
      var pattern = new RegExp(word, 'gi');
      eventDesc = eventDesc.replace(pattern, "<mark class='marked-word'>" + word + '</mark>');
    });
    eventDesc = eventDesc.replace(/\n/g, '<br />');
    return eventDesc;
  }

  /**
   * Generate category string with similar category marked
   */
  markSimilarCategs (category, simCateg) {
    if (!category) return 'no-categ';

    return (category === simCateg) ? ' marked-categ' : '';
  }

  /**
   * Generate category string with similar category marked
   */
  formatFeatures (features) {
    features = features.map(function (feature) {
      return "<span class='features'>" + feature + '</span>';
    });

    return features.join('');
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='event-detail-container'>
        <div className='event-detail-img'>
          <img src={this.props.data.profile_picture} />
        </div>
        <div className='event-detail-text-container'>
          {/* Title + Categories */}
          <div>
            <a className='event-detail-title' href={'https://www.facebook.com/events/' + this.props.data.id} target='_blank'>{this.props.data.name}</a>
            <span className={'event-detail-categ' + this.markSimilarCategs(this.props.data.category, this.props.data.sim_categs)}>
              {this.props.data.category}
            </span>
          </div>
          {/* Date */}
          <div className='event-detail-date'>
            <div className='icon event-date-icon' />
            <p className='event-sub-info'>{this.formatEventTime(this.props.data.start_time, this.props.data.end_time)}</p>
          </div>
          {/* Venue */}
          <div className='event-detail-venue'>
            <div className='icon event-venue-icon' />
            <p className='event-sub-info'>{this.props.data.venue.name}</p>
          </div>
          {/* Stats */}
          <div className='event-detail-stats'>
            <div className='icon event-stats-icon' />
            <p className='event-sub-info'>
              {this.props.data.attending + ' Attending · '}
              {this.props.data.maybe + ' Maybe · '}
              {this.props.data.declined + ' Declined · '}
              {this.props.data.noreply + ' No Reply'}
            </p>
          </div>
          {/* Description */}
          <div className='event-detail-description'>
            <h3>Details</h3>
            <div dangerouslySetInnerHTML={{ __html: this.markSimilarWords(this.props.data.description, this.props.data.sim_words) }} />
          </div>
          {/* Features */}
          <div className='event-detail-features'>
            <div dangerouslySetInnerHTML={{ __html: this.formatFeatures(this.props.data.features) }} />
          </div>
        </div>
        <button
          className='button event-detail-dismiss fa fa-times'
          onClick={this.handleClick} />
      </div>
    );
  }
}

/** Map the redux state to this component's props */
const mapStateToProps = (state) => {
  return {
    allEvents: state._search.results.events.all,
    currentQuery: state._search.query,
    categories: state._search.categories,
    relevant: state._search.results.events.relevant,
    irrelevant: state._search.results.events.irrelevant
  };
};

export default connect(mapStateToProps)(EventDetail);
