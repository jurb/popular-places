var webpack = require('webpack');


module.exports = {
  chainWebpack: (config) => {
    config.plugins.delete('prefetch');
},
  configureWebpack: {
    devServer: {
      host: 'localhost',
      headers: { 'Access-Control-Allow-Origin': '*' }
    }
  }
};
