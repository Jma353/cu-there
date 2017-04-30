import React from 'react';

import { Line } from 'react-chartjs-2';

class TimeGraph extends React.Component {
  render () {
    const datasets = [];
    var index = 1;
    for (var i = 0; i < this.props.data.length; i++) {
      if (this.props.data[i].length) {
        datasets.push({
          backgroundColor: `rgba(${102 - 10 * index}, ${168 - 10 * index}, ${172 - 10 * index}, 0.3)`,
          label: `Dataset number ${index++}`,
          data: this.props.data[i][1].map((y, x) => {
            return {
              x: x,
              y: y
            };
          })
        });
      }
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
