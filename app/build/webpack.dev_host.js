const { merge } = require('webpack-merge')
const common = require('./webpack.config.js')
const webpack = require('webpack')

module.exports = merge(common, {
  mode: 'development',
  plugins: [
    new webpack.DefinePlugin({
      API_URL: JSON.stringify('http://YOUR.IP.ADDRESS.HERE')
    })
  ]
})
