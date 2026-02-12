<template>
  <component :is="currentLayoutComponent">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from './layouts/DefaultLayout.vue'
import BlankLayout from './layouts/BlankLayout.vue'
import FullPageLayout from './layouts/FullPageLayout.vue'

const route = useRoute()

/**
 * 根据路由元信息选择对应的布局组件
 */
const currentLayoutComponent = computed(() => {
  const layout = route.meta?.layout as string

  switch (layout) {
    case 'blank':
      return BlankLayout
    case 'full-page':
      return FullPageLayout
    case 'default':
    default:
      return DefaultLayout
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
