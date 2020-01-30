import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      meta: {keepAlive: true},
      component: (resolve) => {
        require(['../views/index'], resolve)
      }
    },
    {
      path: '/list',
      name: 'listr',
      meta: {keepAlive: false},
      component: (resolve) => {
        require(['../views/list'], resolve)
      }
    },
    {
      path: '/mine',
      name: 'mine',
      meta: {keepAlive: false},
      component: (resolve) => {
        require(['../views/mine'], resolve)
      }
    },
    {
      path: '/error',
      name: 'error',
      meta: {keepAlive: false},
      component: (resolve) => {
        require(['../views/error'], resolve)
      }
    },
    {
      path: '/form',
      name: 'form',
      meta: {keepAlive: false},
      component: (resolve) => {
        require(['../views/form'], resolve)
      }
    }
  ]
})

export default router
