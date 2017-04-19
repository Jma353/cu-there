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
  constructor (props) {
    super(props);

    this.state = {
      query: '',
      results: {
        response: {
          venues: [],
          tags: [],
          times: []
        },
        events: {
          relevant: [],
          irrelevant: []
        }
      }
    };
  }

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
    console.log(this.state);
    const response = this.state.results.response;
    return (
      <div>
        <NavBar query={this.props.location.query.q} />
        <div className='results-header'>
          <p>Showing 42 results</p>
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
