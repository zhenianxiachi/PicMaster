import { computed } from 'vue'
import { useRoute } from 'vue-router'

/**
 * 布局类型
 */
export type LayoutType = 'default' | 'blank' | 'full-page'

/**
 * 布局相关的组合式函数
 */
export function useLayout() {
  const route = useRoute()

  /**
   * 当前路由使用的布局类型
   */
  const currentLayout = computed<LayoutType>(() => {
    const layout = route.meta?.layout as LayoutType
    return layout || 'default'
  })

  /**
   * 是否需要显示头部导航
   */
  const showHeader = computed<boolean>(() => {
    return currentLayout.value === 'default'
  })

  /**
   * 是否需要全屏布局
   */
  const isFullPage = computed<boolean>(() => {
    return currentLayout.value === 'full-page'
  })

  /**
   * 是否需要空白布局
   */
  const isBlank = computed<boolean>(() => {
    return currentLayout.value === 'blank'
  })

  return {
    currentLayout,
    showHeader,
    isFullPage,
    isBlank,
  }
}
