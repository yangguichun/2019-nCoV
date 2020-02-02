module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/static' : '',
  outputDir: process.env.NODE_ENV === 'production' ? '../static' : 'dist',
  indexPath: process.env.NODE_ENV === 'production' ? '../templates/index.html' : 'index.html',
  transpileDependencies: [
    'vue-echarts',
    'resize-detector'
  ],
  devServer: {
    proxy: 'http://127.0.0.1:5000'
    // proxy: 'http://47.107.190.155',
  },
  css: {
    loaderOptions: {
      postcss: {
        plugins: [
          require("postcss-px-to-viewport")({
            unitToConvert: "px",
            viewportWidth: 750,
            unitPrecision: 3,
            propList: [
              "*"
            ],
            viewportUnit: "vw",
            fontViewportUnit: "vw",
            selectorBlackList: [],
            minPixelValue: 1,
            mediaQuery: false,
            replace: true,
            exclude: /(\/|\\)(node_modules)(\/|\\)/,
          })
        ]
      }
    }
  }
}