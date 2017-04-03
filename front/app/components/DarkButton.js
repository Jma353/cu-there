import React from 'react';
import Button from './Button';
require('../../public/sass/DarkButton.scss');

let DarkButton = (props) => {
  return (
    <Button {...props} className={'dark-button ' + props.className} />
  );
};

export default DarkButton;
