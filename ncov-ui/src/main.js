import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import { get, post } from './js/ajax'
import { Button,Tabbar, TabbarItem } from 'vant';
Vue.use(Button);
Vue.use(Tabbar);
Vue.use(TabbarItem);

// import ECharts from 'vue-echarts'
// import 'echarts'
// Vue.component('v-chart', ECharts)

// Vue.prototype.$http = { get, post }
Vue.config.productionTip = false


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
