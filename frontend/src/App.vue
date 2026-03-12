<template>
  <component :is="currentLayoutComponent">
    <router-view />
  </component>
  <AuthDialog />
  <UpgradeDialog />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from './layouts/DefaultLayout.vue'
import BlankLayout from './layouts/BlankLayout.vue'
import FullPageLayout from './layouts/FullPageLayout.vue'
import AuthDialog from './components/AuthDialog.vue'
import UpgradeDialog from './components/UpgradeDialog.vue'

const route = useRoute()

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
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap');

:root {
  --pm-bg: #f6f9fc;
  --pm-surface: #ffffff;
  --pm-surface-soft: #f3f7fb;
  --pm-border: #d7e3ef;
  --pm-text: #11253d;
  --pm-text-soft: #5f738b;
  --pm-primary: #0f7ccf;
  --pm-primary-deep: #09538d;
  --pm-accent: #13b5a8;
  --pm-warm: #f3a644;
  --pm-danger: #dd4f4f;
  --pm-shadow-1: 0 8px 30px rgba(17, 37, 61, 0.08);
  --pm-shadow-2: 0 20px 60px rgba(17, 37, 61, 0.12);
  --pm-radius-lg: 24px;
  --pm-radius-md: 16px;
  --pm-radius-sm: 12px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
}

body {
  font-family: 'Manrope', 'Noto Sans SC', 'PingFang SC', sans-serif;
  color: var(--pm-text);
  background: radial-gradient(circle at 15% 0%, rgba(15, 124, 207, 0.08), transparent 32%), var(--pm-bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1,
h2,
h3,
h4,
h5 {
  font-family: 'Sora', 'Noto Sans SC', 'PingFang SC', sans-serif;
}
</style>
