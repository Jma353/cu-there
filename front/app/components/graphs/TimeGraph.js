import React from 'react';

import { Line } from 'react-chartjs-2';

class TimeGraph extends React.Component {
  render () {
    const datasets = [];

    // Handle projected attendance
    for (var i = 0; i < this.props.data.length; i++) {
      datasets.push({
        fill: false,
        backgroundColor: `rgb(${102 - 20 * i}, ${168 - 20 * i}, ${172 - 20 * i})`,
        borderColor: `rgb(${102 - 20 * i}, ${168 - 20 * i}, ${172 - 20 * i})`,
        borderWidth: 1,
        label: this.props.data[i].venue_name,
        data: this.props.data[i].projected_attendance.map((y, x) => {
          return {
            x: x,
            y: y
          };
        })
      });

      // datasets.push({
      //   backgroundColor: 'red',
      //   label: this.props.data[i].venue_name + ' PEAK',
      //   data: this.props.data[i].event_times.map((event, x) => {
      //     return {
      //       x: x,
      //       y: event.time.index
      //     };
      //   })
      // });
    }

    const data = {
      datasets: datasets
    };

    return (
      <div>
        <p>Time Graph</p>
        <Line
          data={data}
          options={{
            scales: {
              xAxes: [{
                type: 'linear',
                position: 'bottom'
              }]
            }
          }}
          />
      </div>
    );
  }
}

export default TimeGraph;
