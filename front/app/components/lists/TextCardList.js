import React from 'react';
import TextCard from '../cards/TextCard';
require('../../../public/sass/TextCardList.scss');

class TextCardList extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.generateCard = this.generateCard.bind(this);
  }

  /**
   * Generate a text card
   */
  generateCard (text, i) {
    return <TextCard text={text} key={i} />;
  }

  /**
   * Render
   */
  render () {
    let textCards = this.props.info.map(this.generateCard);
    return (
      <div>
        <div className='text-card-list-title'>
          {this.props.title}
        </div>
        <div className='text-card-list'>
          {textCards}
        </div>
      </div>
    );
  }
}

export default TextCardList;
