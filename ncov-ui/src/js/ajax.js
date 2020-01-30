import axios from 'axios'
import vm from '../main'
// import Vue from 'vue'

const PRODUCT_URL = 'https://xxxx.com'
const MOCK_URL = 'http://mock.com'
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

function get (url) {
  return new Promise((resolve, reject) => {
    http.get(url)
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

function post (url, data, loading) {
  return new Promise((resolve, reject) => {
    http.post(url, data, { loading: loading })
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

export default { get, post }
