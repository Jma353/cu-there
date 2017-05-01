import React from 'react';
import { formatTime } from '../../utils/time';
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
        pointRadius: 0,
        pointHitRadius: 0,
        data: this.props.data[i].regression.map((y, x) => { return { x: x, y: y }; })
      });

      const peak = this.props.data[i].peak;
      datasets.push({
        fill: false,
        backgroundColor: 'red',
        borderWidth: 1,
        label: 'PEAK',
        data: [{
          x: peak,
          y: 0
        }]
      });
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
                position: 'bottom',
                ticks: {
                  callback: function (label, index, labels) {
                    return formatTime(label);
                  }
                },
                scaleLabel: {
                  display: true,
                  labelString: 'Time of Day'
                }
              }],
              yAxes: [{
                ticks: {
                  min: 0
                },
                scaleLabel: {
                  display: true,
                  labelString: 'Attendance'
                }
              }]
            },
            legend: {
              display: false
            }
          }}
          />
      </div>
    );
  }
}

export default TimeGraph;
