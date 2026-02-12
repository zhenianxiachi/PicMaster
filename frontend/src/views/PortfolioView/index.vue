<template>
  <div class="portfolio-view-container">
    <div class="hero-section">
      <h2 class="hero-title">作品集管理</h2>
      <p class="hero-subtitle">创建、编辑和管理您的摄影作品集</p>
    </div>

    <div class="content-area">
      <PortfolioManager />
    </div>
  </div>
</template>

<script setup lang="ts">
import PortfolioManager from '@/components/PortfolioManager.vue'
</script>

<style scoped>
.portfolio-view-container {
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