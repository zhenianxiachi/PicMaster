<template>
  <div class="viewer-view-container">
    <div class="hero-section">
      <h2 class="hero-title">作品集展示</h2>
      <p class="hero-subtitle">以多种布局方式展示您的精彩作品</p>
    </div>

    <div class="content-area">
      <PortfolioViewer :initial-portfolio-id="initialPortfolioId" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PortfolioViewer from '@/components/PortfolioViewer.vue'

const initialPortfolioId = ref<number | null>(null)

onMounted(() => {
  // 从URL参数中获取portfolio_id
  const urlParams = new URLSearchParams(window.location.search)
  const portfolioIdParam = urlParams.get('portfolio_id')
  if (portfolioIdParam) {
    initialPortfolioId.value = parseInt(portfolioIdParam)
  }
})
</script>

<style scoped>
.viewer-view-container {
  padding: 0 24px 80px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.hero-section {
  text-align: center;
  padding: 80px 24px 60px;
  animation: fadeInUp 0.8s ease-out;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  color: #1d1d1f;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin-bottom: 12px;
}

.hero-subtitle {
  font-size: 24px;
  font-weight: 400;
  color: #86868b;
  letter-spacing: 0.01em;
}

.content-area {
  animation: fadeInUp 0.6s ease-out 0.2s both;
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

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 16px 40px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }
}
</style>
