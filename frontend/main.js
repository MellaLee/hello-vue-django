import Vue from 'vue';
import ElementUI from 'element-ui';
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import $router from './router.js';
import $store from './mods/store';
import '../static/font/iconfont.css';

Vue.use(ElementUI);
Vue.use(VueResource);

function getCookie(name) {
    let arr,
        reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)")
    if (arr = document.cookie.match(reg)) {
        return decodeURIComponent(arr[2])
    }
}

// 设置 POST 请求时 的 data 格式
Vue.http.options.emulateJSON = true

// 设置 X-CSRFToken
Vue.http.interceptors.push(function (request, next) {
    request.method = 'POST'
    request.headers.set('X-CSRFToken', getCookie('csrftoken'))
    next()
})
  
new Vue({
  el: '#app',
  router: $router,
  store: $store,
  render: h => h(App)
});