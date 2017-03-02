module.exports = {
  entry: [
    './public/main.js'
  ],
  output: {
    path: '../app/template',
    filename: 'bundle.js'
  }, module: {
    loaders: [{
      test: /\.jsx?$/,
      loader: 'babel-loader',
      query: {
        presets: ['es2015', 'react']
      }
    }]
  }
};
