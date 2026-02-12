<template>
  <div class="blank-layout">
    <slot />
  </div>
</template>

<script setup lang="ts">
// 空白布局，不包含任何头部导航
</script>

<style scoped>
.blank-layout {
  min-height: 100vh;
  width: 100%;
}
</style>
