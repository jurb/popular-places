var webpack = require('webpack');

// module.exports = {
//   configureWebpack: {
//     plugins: [
//       new webpack.ProvidePlugin({
//         mapboxgl: "mapbox-gl"
//       })
//     ]
//   }
// };

module.exports = {
  configureWebpack: {
    devServer: {
      host: 'localhost',
      headers: { 'Access-Control-Allow-Origin': '*' }
    }
  }
};
