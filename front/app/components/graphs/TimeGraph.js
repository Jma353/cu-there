import React from 'react';
import { formatTime } from '../../utils/time';
import { Line } from 'react-chartjs-2';

class TimeGraph extends React.Component {
  render () {
    const datasets = [];

    // Handle projected attendance
    for (var i = 0; i < this.props.data.length; i++) {
      const peak = this.props.data[i].peak;
      const peakValue = this.props.data[i].peak_value;

      datasets.push({
        fill: false,
        backgroundColor: 'rgba(87, 133, 137, 1.0)',
        borderWidth: 1,
        label: 'PEAK',
        data: [{
          x: peak,
          y: peakValue
        }]
      });

      datasets.push({
        backgroundColor: `rgba(102, 168, 172, 0.1)`,
        borderColor: `rgba(102, 168, 172, 0.5)`,
        borderWidth: 1,
        pointRadius: 0,
        pointHitRadius: 0,
        data: this.props.data[i].regression.map((y, x) => { return { x: x, y: y }; })
      });
    }

    const data = {
      datasets: datasets
    };

    return (
      <div className='time-graph'>
        <h2>Time Graph</h2>
        <Line
          data={data}
          options={{
            responsive: true,
            scales: {
              xAxes: [{
                type: 'linear',
                position: 'bottom',
                ticks: {
                  callback: function (label, index, labels) {
                    return formatTime(label);
                  },
                  max: 23
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
            },
            tooltips: {
              callbacks: {
                title: function (tooltipItem, data) {
                  return null;
                },
                label: function (tooltipItem, data) {
                  return 'Peak: ' + formatTime(tooltipItem.xLabel);
                }
              }
            }
          }}
          />
      </div>
    );
  }
}

export default TimeGraph;
