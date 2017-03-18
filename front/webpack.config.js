const path = require('path');
const staticDIR = path.join(__dirname, '../app/static/') // where we put everything
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const extractSASS = new ExtractTextPlugin('css/styles.css');

module.exports = {
  entry: [
    './browser.js'
  ],
  output: {
    path: staticDIR,
    publicPath: 'static/',
    filename: 'js/bundle.js'
  },
  devServer: {
    contentBase: path.join(__dirname, '../app/templates'),
    historyApiFallback: true,
    port: 3000
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
