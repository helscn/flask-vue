import Vue from 'vue'
import axios from 'axios'
import App from './App.vue'

axios.defaults.timeout = 5000
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
axios.defaults.baseURL = 'http://localhost:5000'

Vue.prototype.axios = axios
Vue.config.productionTip = false

new Vue({
    render: h => h(App),
}).$mount('#app')
