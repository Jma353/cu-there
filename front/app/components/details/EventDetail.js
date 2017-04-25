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
      actionCreators.didChangeRelevance(this.props.currentQuery, relevant, irrelevant, all)
    );
  }

  /**
   * Format date
   */
  formatDate (d) {
    var date = new Date(d)
    var hours = date.getHours()
    var mins = date.getMinutes()
    var ampm = (hours >= 12) ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12;
    mins = (mins < 10) ? '0' + mins : mins;
    var time = hours + ':' + mins + ' ' + ampm;

    var monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    return (monthNames[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear() + ' ' + time);
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
          {/* Title */}
          <a className='event-detail-title' href={'https://www.facebook.com/events/' + this.props.data.id} target='_blank'>
            {this.props.data.name} - {this.props.data.category}
          </a>
          {/* Venue */}
          <div className='event-detail-venue'>
            <p>{this.props.data.venue_id}</p>
          </div>
          {/* Date */}
          <div className='event-detail-date'>
            <p>{this.formatDate(this.props.data.start_time)} - {this.formatDate(this.props.data.end_time)}</p>
          </div>
          {/* Description */}
          <div className='event-detail-description'>
            {this.props.data.description}
          </div>
          {/* Stats */}
          <div className='event-detail-stats'>
            {'Attending: ' + this.props.data.attending + '\n'}
            {'No Reply: ' + this.props.data.noreply + '\n'}
            {'Declined: ' + this.props.data.declined + '\n'}
            {'Maybe: ' + this.props.data.maybe}
          </div>
          {/* Similar Tags */}
          <div className='event-detail-stats'>
            {'Similar Words: ' + this.props.data.sim_words.join(', ') + '\n'}
            {'Similar Categories: ' + this.props.data.sim_categs}
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
    relevant: state._search.results.events.relevant,
    irrelevant: state._search.results.events.irrelevant
  };
};

export default connect(mapStateToProps)(EventDetail);
