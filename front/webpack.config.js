const staticDIR = '../app/static/' // where we put everything
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const extractSASS = new ExtractTextPlugin('css/styles.css');

module.exports = {
  entry: [
    './browser.js'
  ],
  output: {
    path: staticDIR,
    filename: 'js/bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        }
      },
      {
        test: /\.scss$/,
        use: extractSASS.extract({ use: 'css-loader!sass-loader' })
      }
    ]
  },
  plugins: [
    extractSASS
  ]
};
