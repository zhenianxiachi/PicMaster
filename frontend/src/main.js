import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from 'axios'

const app = createApp(App)
app.use(ElementPlus)

// 配置axios全局默认值
axios.defaults.baseURL = '/api'
axios.defaults.timeout = 10000

app.config.globalProperties.$axios = axios
app.mount('#app')