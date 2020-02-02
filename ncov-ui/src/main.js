import Vue from 'vue'
import App from './App.vue'
import router from './router'

// https://github.com/imcvampire/vue-axios
// import axios from 'axios'
// import VueAxios from 'vue-axios'
// Vue.use(VueAxios, axios)
import VueResource from 'vue-resource'
Vue.use(VueResource);


import { Button,Tabbar, TabbarItem,Tag, Col, Row, Grid, GridItem, Icon, Toast, Picker, Field, Popup} from 'vant';
Vue.use(Button);
Vue.use(Tabbar);
Vue.use(TabbarItem);
Vue.use(Tag);
Vue.use(Col);
Vue.use(Row);
Vue.use(Grid);
Vue.use(GridItem);
Vue.use(Icon);
Vue.use(Toast);
Vue.use(Picker);
Vue.use(Field);
Vue.use(Popup);

// import ECharts from 'vue-echarts'
// import 'echarts'
// Vue.component('v-chart', ECharts)

// Vue.prototype.$http = { get, post }
Vue.config.productionTip = false


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
