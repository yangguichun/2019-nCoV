// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { get, post } from './JS/ajax'
import utils from './JS/utils'
// import vConsole from './JS/vconsole'
import toast from './components/toast'
import Dialog from './components/dialog'
import Loading from './components/loading'

import VueScroller from 'vue-scroller'

Vue.use(VueScroller)
Vue.use(utils)
// Vue.use(vConsole)

Vue.prototype.$toast = toast
Vue.prototype.$dialog = Dialog
Vue.prototype.$loading = Loading
Vue.prototype.$axios = { get, post }

Vue.config.productionTip = false

let cale = window.screen.availWidth > 750 ? 2 : window.screen.availWidth / 375
window.document.documentElement.style.fontSize = `${100 * cale}px`

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
