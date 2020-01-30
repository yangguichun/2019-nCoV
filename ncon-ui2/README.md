# vue-mobile

## 简介

vue-mobile 是是基于 vue-cli 实现的移动端 H5 开发模板，其中已经搭建好基本的开发框架，可帮助您实现快速开发。
技术栈：vue + vux + axios + less

## 功能

- 搭建项目目录
- 配置 css 预处理器
- 配置 UI 组件库 vux
- 解决移动端适配
- 配置页面路由缓存
- axios 请求封装
- 工具类函数封装
- toast 组件封装
- dialog 组件封装
- 底部导航组件封装
- 列表页 demo
- 表单页 demo

### 搭建项目目录

按如下文件目录搭建项目框架

```
src                               主要源码目录
|-- assets                        静态资源，统一管理
|-- components                    公用组件，全局组件
|-- javascript                    JS相关操作处理
    |-- ajax                      axios封装的请求拦截
    |-- utils                     全局封装的工具类
    |-- datas                     模拟数据，临时存放
|-- router                        路由，统一管理
|-- store                         vuex, 统一管理
|-- views                         视图目录
```

### 配置 css 预处理器

1. 安装依赖

```
npm install less less-loader --sava-dev
```

2. 在 build/webpack.base.conf.js 里参照如下代码进行配置

```js
{
  test: /\.less$/,
  loader: "style-loader!css-loader!less-loader"
}
```

### 配置 vux

1. 安装依赖

```
npm install vux vux-loader --save
```

2. 在 build/webpack.base.conf.js 里参照如下代码进行配置

```js
const vuxLoader = require('vux-loader') //把vux-loader引入
module.exports = vuxLoader.merge(webpackConfig, {
  //把新旧配置进行merge（放到页面最底部）
  plugins: ['vux-ui']
})
```

3. 局部注册使用

```js
;<group>
  <cell title="title" value="value" />
</group>

import { Group, Cell } from 'vux' //引入所需组件
export default {
  name: 'App',
  components: {
    //注册组件
    Group,
    Cell
  }
}
```

### 移动端适配

1. 安装依赖

```
npm install px2rem-loader --save-dev
```

2. 在 build/utils 进行如下配置

```js
const px2remLoader = {
  loader: 'px2rem-loader',
  options: {
    remUnit: 100
  }
}

function generateLoaders(loader, loaderOptions) {
  const loaders = options.usePostCSS ? [cssLoader, postcssLoader, px2remLoader] : [cssLoader, px2remLoader]

  if (loader) {
    loaders.push({
      loader: loader + '-loader',
      options: Object.assign({}, loaderOptions, {
        sourceMap: options.sourceMap
      })
    })
  }

  // Extract CSS when that option is specified
  // (which is the case during production build)
  if (options.extract) {
    return ExtractTextPlugin.extract({
      use: loaders,
      fallback: 'vue-style-loader'
    })
  } else {
    return ['vue-style-loader'].concat(loaders)
  }
}
```

3. 在 main.js 设置 html 跟字体大小

```js
let cale = window.screen.availWidth > 750 ? 2 : window.screen.availWidth / 375
window.document.documentElement.style.fontSize = `${100 * cale}px`
```

这是最简单的适配方法，后续跟单独对移动端 rem 适配做详细解读。

### 路由配置

1. 通过配置路由对象的 meta[keepAlive]值来区分页面是否需要缓存

```js
routes: [
  {
    path: '/',
    name: 'index',
    meta: { keepAlive: true }, //需要缓存
    component: resolve => {
      require(['../views/index'], resolve)
    }
  },
  {
    path: '/list',
    name: 'listr',
    meta: { keepAlive: false }, //不需要缓存
    component: resolve => {
      require(['../views/list'], resolve)
    }
  }
]
```

2. 在 app.vue 做缓存判断

```html
<div id="app">
  <router-view v-if="!$route.meta.keepAlive"></router-view>
  <keep-alive>
    <router-view v-if="$route.meta.keepAlive"></router-view>
  </keep-alive>
</div>
```

### axios 请求封装

1. 设置请求拦截和响应拦截

```js
const PRODUCT_URL = 'https://xxxx.com'
const MOCK_URL = 'http://xxxx.com'
let http = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? PRODUCT_URL : MOCK_URL
})
// 请求拦截器
http.interceptors.request.use(
  config => {
    // 设置token，Content-Type
    var token = sessionStorage.getItem('UserLoginToken')
    config.headers['token'] = token
    config.headers['Content-Type'] = 'application/json;charset=UTF-8'
    // 请求显示loading效果
    if (config.loading === true) {
      vm.$loading.show()
    }
    return config
  },
  error => {
    vm.$loading.hide()
    return Promise.reject(error)
  }
)
// 响应拦截器
http.interceptors.response.use(
  res => {
    vm.$loading.hide()
    // token失效，重新登录
    if (res.data.code === 401) {
      //  重新登录
    }
    return res
  },
  error => {
    vm.$loading.hide()
    return Promise.reject(error)
  }
)
```

2. 封装 get 和 post 请求方法

```js
function get(url, data, lodaing) {
  return new Promise((resolve, reject) => {
    http
      .get(url)
      .then(
        response => {
          resolve(response)
        },
        err => {
          reject(err)
        }
      )
      .catch(error => {
        reject(error)
      })
  })
}

function post(url, data, loading) {
  return new Promise((resolve, reject) => {
    http
      .post(url, data, { loading: loading })
      .then(
        response => {
          resolve(response)
        },
        err => {
          reject(err)
        }
      )
      .catch(error => {
        reject(error)
      })
  })
}

export { get, post }
```

3. 把 get，post 方法挂载到 vue 实例上。

```js
// main.js
import { get, post } from './js/ajax'
Vue.prototype.$http = { get, post }
```

### 工具类函数封装

1. 添加方法到 vue 实例的原型链上

```js
export default {
  install (Vue, options) {
    Vue.prototype.util = {
      method1(val) {
        ...
      },
      method2 (val) {
       ...
      },
  }
}
```

2. 在 main.js 通过 vue.use()注册

```js
import utils from './js/utils'
Vue.use(utils)
```
