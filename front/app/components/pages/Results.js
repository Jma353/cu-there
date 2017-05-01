import React from 'react';
import NavBar from '../navigation/NavBar';
import VenueDetailList from '../lists/VenueDetailList';
import EventDetailList from '../lists/EventDetailList';
import TextCardList from '../lists/TextCardList';
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
   * Render
   */
  render () {
    console.log(this.props);
    const response = this.props.results.response;
    const categories = this.props.location.query.categs;

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
            <div className='result-times'>
              <TimeGraph data={response.graphs} />
            </div>
            <div className='result-features'>
              <TextCardList data={response.features} title='Suggested Features' />
            </div>
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
