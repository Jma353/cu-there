
  /**
   * Format time to 12 hour system
   */
var formatTime = function (times) {
  var formattedTimes = [];

  times = times.map(function (e) {
    return e.split(':');
  });

  // Sort times array
  times = times.sort(function (a, b) {
    if (a[0] < b[0]) { // Earlier hour
      return -1;
    } else if (a[0] > b[0]) { // Later hour
      return 1;
    }

    // Same hour, so compare minutes
    if (a[1] < b[1]) { // Earlier minutes
      return -1;
    } else if (a[1] > b[1]) { // Later minutes
      return 1;
    }

    return 0;
  });

  for (var i = 0; i < times.length; i++) {
    var hour = times[i][0];
    var min = times[i][1];
    var ampm = (hour >= 12) ? 'PM' : 'AM';
    hour = (hour % 12) || 12;
    var time = hour + ':' + min + ' ' + ampm;

    if (!formattedTimes.includes(time)) {
      formattedTimes.push(time);
    }
  }

  return (formattedTimes);
};

export { formatTime };
