import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import global from './assets/global.js'


import axios from 'axios'
Vue.prototype.$axios = axios
Vue.prototype.global = global
// axios.defaults.baseURL = '/api'
// axios.defaults.headers.post['Content-Type'] = 'application/json';
// import VueAxios from 'vue-axios'
// Vue.prototype.$axios = axios


Vue.use(ElementUI);

Vue.config.productionTip = false

export const eventBus = new Vue()



new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
