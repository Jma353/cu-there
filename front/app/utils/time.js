
/**
 * Format times to 12 hour system
 */
var formatTime = function (time) {
  time = [time, '00'];
  var hour = time[0] % 24;
  var min = time[1];
  var ampm = (hour >= 12) ? 'PM' : 'AM';
  hour = (hour % 12) || 12;
  return hour + ':' + min + ' ' + ampm;
};

export { formatTime };
