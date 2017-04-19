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
    console.log(all.length);

    let ids = all.map(a => { return a.id; });
    console.log(ids);
    console.log(this.props.data.id);
    let i = ids.indexOf(this.props.data.id);
    console.log(i);
    let removed = all.splice(i, 1);
    console.log(removed);
    console.log(all.length);

    // Dispatch this event b/c relevance changed
    this.props.dispatch(
      actionCreators.didChangeRelevance(this.props.currentQuery, relevant, irrelevant, all)
    );
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
          <div className='event-detail-title'>
            {this.props.data.name}
          </div>
          {/* Venue */}
          <div className='event-detail-venue'>
            <p>{this.props.data.venue}</p>
          </div>
          {/* Date */}
          <div className='event-detail-date'>
            <p>{this.props.data.date}</p>
          </div>
          {/* Description */}
          <div className='event-detail-description'>
            {this.props.data.description}
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
