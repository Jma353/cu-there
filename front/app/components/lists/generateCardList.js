import React from 'react';

/**
 * Generate a Card List
 */
export default function generateCardList (WrappedList, WrappedCard) {
  return class extends React.Component {

    /**
     * Constructor
     */
    constructor (props) {
      super(props);
      this.generateCard = this.generateCard.bind(this);
    }

    /**
     * Generate a card
     */
    generateCard (data, i) {
      return <WrappedCard data={data} key={i} id={i} />;
    }

    /**
     * Render
     */
    render () {
      let cards = this.props.data.map(this.generateCard);
      return (
        <WrappedList cards={cards} {...this.props} />
      );
    }
  };
}
