<template>
  <div class="full-page-layout">
    <slot />
  </div>
</template>

<script setup lang="ts">
// 全屏布局，用于首页等特殊页面
</script>

<style scoped>
.full-page-layout {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}
</style>
