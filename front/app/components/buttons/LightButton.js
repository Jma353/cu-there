import React from 'react';
import Button from './Button';
require('../../../public/sass/LightButton.scss');

let LightButton = (props) => {
  return (
    <Button {...props} className={'light-button ' + props.className} />
  );
};

export default LightButton;
