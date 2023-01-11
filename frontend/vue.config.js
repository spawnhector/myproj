let port = 8081;
module.exports = {
  runtimeCompiler: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/static/dist/' : `http://127.0.0.1:${port}`,
  outputDir: '../backend/static/dist',
  indexPath: '../../templates/base-vue.html',
  
  devServer: {
    host: '127.0.0.1',
    port: port,
    devMiddleware: {
      writeToDisk: true,
    },
    headers: {"Access-Control-Allow-Origin": "*"},
    hot: true,
  },

  transpileDependencies: [
    'vuetify'
  ]
}
