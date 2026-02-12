<template>
  <div class="home-view-container">
    <!-- Hero 广告区域 -->
    <div class="hero-banner">
      <div class="hero-content">
        <h1 class="hero-title">PicMaster</h1>
        <p class="hero-subtitle">专业的图片编辑与作品集管理平台</p>
        <div class="hero-buttons">
          <button class="btn-primary" @click="goToEditor">开始编辑</button>
          <button class="btn-secondary" @click="goToViewer">浏览作品</button>
        </div>
      </div>
    </div>

    <!-- 特性展示区域 -->
    <div class="features-section">
      <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <h3 class="feature-title">专业编辑</h3>
        <p class="feature-desc">强大的图片编辑功能，轻松打造精美作品</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📁</div>
        <h3 class="feature-title">作品集管理</h3>
        <p class="feature-desc">创建和管理您的个人作品集，展示创意</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🖼️</div>
        <h3 class="feature-title">沉浸式浏览</h3>
        <p class="feature-desc">优雅的作品展示方式，极致的浏览体验</p>
      </div>
    </div>

    <!-- 广告宣传语 -->
    <div class="promo-section">
      <div class="promo-card">
        <h2 class="promo-title">立即体验 PicMaster</h2>
        <p class="promo-desc">发现无限创意可能</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

/**
 * 跳转到编辑介绍页面
 */
function goToEditor(): void {
  router.push('/editor-intro')
}

/**
 * 跳转到作品展示页面
 */
function goToViewer(): void {
  router.push('/viewer')
}
</script>

<style scoped>
.home-view-container {
  width: 100%;
  min-height: calc(100vh - 72px);
  background: #ffffff;
}

/* Hero Banner */
.hero-banner {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #f8f9fa;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  animation: fadeInUp 1s ease-out;
}

.hero-title {
  font-size: 72px;
  font-weight: 800;
  color: #1d1d1f;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 24px;
}

.hero-subtitle {
  font-size: 28px;
  font-weight: 400;
  color: #86868b;
  letter-spacing: 0.02em;
  margin-bottom: 48px;
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 16px 40px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
}

.btn-primary {
  background: #007aff;
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.btn-secondary {
  background: #ffffff;
  color: #007aff;
  border: 2px solid #007aff;
}

.btn-secondary:hover {
  background: #f0f7ff;
  transform: translateY(-2px);
}

/* Features Section */
.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  padding: 80px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #ffffff;
  padding: 48px 32px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease-out 0.2s both;
  border: 1px solid #e5e5e7;
}

.feature-card:nth-child(2) {
  animation-delay: 0.4s;
}

.feature-card:nth-child(3) {
  animation-delay: 0.6s;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.feature-title {
  font-size: 24px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 12px;
}

.feature-desc {
  font-size: 16px;
  font-weight: 400;
  color: #86868b;
  line-height: 1.6;
}

/* Promo Section */
.promo-section {
  padding: 60px 24px;
  max-width: 1200px;
  margin: 0 auto 80px;
}

.promo-card {
  background: #f8f9fa;
  padding: 60px 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.8s ease-out 0.8s both;
  border: 1px solid #e5e5e7;
}

.promo-title {
  font-size: 36px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 16px;
}

.promo-desc {
  font-size: 24px;
  font-weight: 400;
  color: #86868b;
}

/* Animations */
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
  .hero-banner {
    min-height: 70vh;
    padding: 32px 16px;
  }

  .hero-title {
    font-size: 48px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    max-width: 280px;
  }

  .features-section {
    grid-template-columns: 1fr;
    padding: 60px 16px;
  }

  .promo-title {
    font-size: 28px;
  }

  .promo-desc {
    font-size: 18px;
  }
}
</style>
