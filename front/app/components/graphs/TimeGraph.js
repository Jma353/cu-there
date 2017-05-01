import React from 'react';

import { Line } from 'react-chartjs-2';

class TimeGraph extends React.Component {
  render () {
    const datasets = [];

    // Handle projected attendance
    for (var i = 0; i < this.props.data.length; i++) {
      datasets.push({
        fill: false,
        backgroundColor: `rgba(${102 - 20 * i}, ${168 - 20 * i}, ${172 - 20 * i}, 0.5)`,
        borderColor: `rgba(${102 - 20 * i}, ${168 - 20 * i}, ${172 - 20 * i}, 0.5)`,
        borderWidth: 1,
        data: this.props.data[i].map((y, x) => { return { x: x, y: y }; })
      });
    }

      // datasets.push({
      //   fill: false,
      //   backgroundColor: 'red',
      //   borderWidth: 1,
      //   label: this.props.data[i].venue_name + ' PEAK',
      //   data: this.props.data[i].event_times.map((event, x) => {
      //     return {
      //       x: event.time,
      //       y: event.attendance || 0
      //     };
      //   })
      // });

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
            },
            legend: {
              display: true
            }
          }}
          />
      </div>
    );
  }
}

export default TimeGraph;
