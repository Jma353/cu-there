import React from 'react';

/**
 * Reusable Button Component
 */
class Button extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <button
        className={'button ' + this.props.className}
        onClick={this.props.onClick || (() => {})}>
        {this.props.value}
      </button>
    );
  }
}

export default Button;
