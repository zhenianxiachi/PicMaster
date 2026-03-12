import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'
import { useUsageStore } from './store/usage'
import '@/styles/index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(ElementPlus)
app.use(router)

// 初始化认证状态
const authStore = useAuthStore()
authStore.initializeAuth()
const usageStore = useUsageStore()
usageStore.initializeUsage()

app.mount('#app')
