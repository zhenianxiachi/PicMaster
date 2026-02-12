<template>
  <div class="editor-intro-container">
    <!-- 介绍内容区域 -->
    <div class="intro-content">
      <h1 class="intro-title">图片编辑功能</h1>
      <div class="intro-features">
        <div class="feature-item">
          <h2 class="feature-text">专业滤镜效果</h2>
        </div>
        <div class="feature-item">
          <h2 class="feature-text">智能裁剪工具</h2>
        </div>
        <div class="feature-item">
          <h2 class="feature-text">亮度对比度调整</h2>
        </div>
        <div class="feature-item">
          <h2 class="feature-text">色彩饱和度优化</h2>
        </div>
        <div class="feature-item">
          <h2 class="feature-text">实时预览编辑</h2>
        </div>
        <div class="feature-item">
          <h2 class="feature-text">一键导出保存</h2>
        </div>
      </div>
      <div class="intro-action">
        <button class="start-edit-btn" @click="goToEditor">开始编辑</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

/**
 * 跳转到图片编辑页面
 */
function goToEditor(): void {
  router.push('/editor')
}
</script>

<style scoped>
.editor-intro-container {
  width: 100%;
  min-height: calc(100vh - 72px);
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.intro-content {
  max-width: 800px;
  text-align: center;
  animation: fadeInUp 0.8s ease-out;
}

.intro-title {
  font-size: 56px;
  font-weight: 800;
  color: #1d1d1f;
  letter-spacing: -0.03em;
  line-height: 1.2;
  margin-bottom: 60px;
}

.intro-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 60px;
}

.feature-item {
  padding: 32px 24px;
  background: #f5f5f7;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  background: #ffffff;
}

.feature-text {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.01em;
  margin: 0;
  line-height: 1.4;
}

.intro-action {
  display: flex;
  justify-content: center;
}

.start-edit-btn {
  padding: 20px 60px;
  font-size: 22px;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
  background: #007aff;
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
}

.start-edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
  background: #0066e6;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .intro-title {
    font-size: 40px;
    margin-bottom: 40px;
  }

  .intro-features {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-bottom: 40px;
  }

  .feature-item {
    padding: 20px 16px;
  }

  .feature-text {
    font-size: 16px;
  }

  .start-edit-btn {
    padding: 16px 48px;
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .intro-features {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .feature-text {
    font-size: 18px;
  }
}
</style>
