import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

interface RouteMeta {
  title?: string
  layout?: 'default' | 'blank' | 'full-page'
  requiresAuth?: boolean
  [key: string]: unknown
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView/index.vue'),
    meta: { title: '首页', layout: 'default' } as RouteMeta,
  },
  {
    path: '/editor-intro',
    name: 'EditorIntro',
    component: () => import('../views/EditorIntroView/index.vue'),
    meta: { title: '编辑控制台', layout: 'default' } as RouteMeta,
  },
  {
    path: '/editor',
    name: 'Editor',
    component: () => import('../views/EditorView/index.vue'),
    meta: { title: '在线编辑器', layout: 'full-page' } as RouteMeta,
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: () => import('../views/PortfolioView/index.vue'),
    meta: { title: '作品集管理', layout: 'default', requiresAuth: true } as RouteMeta,
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: () => import('../views/ViewerView/index.vue'),
    meta: { title: '作品展示', layout: 'default' } as RouteMeta,
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: () => import('../views/PrivacyPolicyView/index.vue'),
    meta: { title: '隐私政策', layout: 'default' } as RouteMeta,
  },
  {
    path: '/terms-of-service',
    name: 'TermsOfService',
    component: () => import('../views/TermsOfServiceView/index.vue'),
    meta: { title: '服务条款', layout: 'default' } as RouteMeta,
  },
  {
    path: '/business-cooperation',
    name: 'BusinessCooperation',
    component: () => import('../views/BusinessCooperationView/index.vue'),
    meta: { title: '商务合作', layout: 'default' } as RouteMeta,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const meta = to.meta as RouteMeta
  document.title = meta.title ? `${meta.title} - PicMaster` : 'PicMaster'

  if (meta.requiresAuth && !authStore.isLoggedIn) {
    authStore.openAuthDialog('login')
    ElMessage.warning('请先登录后再进入该模块')
    next({ path: '/' })
    return
  }

  next()
})

export default router
