import { createRouter, createWebHistory } from 'vue-router'

/**
 * 路由元信息接口
 */
interface RouteMeta {
  title?: string
  layout?: 'default' | 'blank' | 'full-page'
  [key: string]: any
}

/**
 * 路由配置
 */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView/index.vue'),
    meta: { title: '首页', layout: 'default' },
  },
  {
    path: '/editor-intro',
    name: 'EditorIntro',
    component: () => import('../views/EditorIntroView/index.vue'),
    meta: { title: '编辑介绍', layout: 'default' },
  },
  {
    path: '/editor',
    name: 'Editor',
    component: () => import('../views/EditorView/index.vue'),
    meta: { title: '图片编辑', layout: 'full-page' },
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: () => import('../views/PortfolioView/index.vue'),
    meta: { title: '作品集管理', layout: 'default' },
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: () => import('../views/ViewerView/index.vue'),
    meta: { title: '作品集展示', layout: 'default' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/**
 * 全局前置守卫，设置页面标题
 */
router.beforeEach((to, _from, next) => {
  const meta = to.meta
  document.title = meta.title ? `${meta.title} - PicMaster` : 'PicMaster'
  next()
})

export default router
