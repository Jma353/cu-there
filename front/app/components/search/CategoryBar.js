import React from 'react';

require('../../../public/sass/CategoryBar.scss');

class CategoryBar extends React.Component {

  handleAdd () {
    
  }

  render () {
    const categories = this.props.categories.map((c, i) =>
      <li key={i}>
        <span>{c}</span>
        <button className='fa fa-times' onClick={this.props.onItemClick(i)} />
      </li>
    );

    return (
      <div className='category-bar'>
        <span className='category-label'>Categories:</span>
        <ul>
          {categories}
          <li className='category-add' onClick={() => this.handleAdd()}>
            <button className='fa fa-plus' />
            <span>Add Category</span>
          </li>
        </ul>
      </div>
    );
  }
}

export default CategoryBar;
