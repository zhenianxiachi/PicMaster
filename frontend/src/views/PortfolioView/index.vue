<template>
  <div class="portfolio-view">
    <section class="hero-banner">
      <div class="hero-copy">
        <p class="eyebrow">PORTFOLIO WORKSPACE</p>
        <h1>作品集管理中心</h1>
        <p>
          面向商业交付场景集中管理项目作品、客户信息与图像素材，支持快速编辑、批量上传与安全归档。
        </p>
      </div>
      <div class="hero-badges">
        <span>Studio-grade</span>
        <span>Client-ready</span>
        <span>Brand-consistent</span>
      </div>
    </section>

    <section class="manager-shell">
      <PortfolioManager />
    </section>
  </div>
</template>

<script setup lang="ts">
import PortfolioManager from '@/components/PortfolioManager.vue'
</script>

<style scoped>
.portfolio-view {
  min-height: calc(100vh - 122px);
  padding: 22px 24px 56px;
}

.hero-banner,
.manager-shell {
  max-width: 1320px;
  margin: 0 auto;
}

.hero-banner {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-lg);
  background:
    radial-gradient(circle at 90% 0%, rgba(15, 124, 207, 0.16), transparent 42%),
    radial-gradient(circle at 0% 90%, rgba(19, 181, 168, 0.12), transparent 34%),
    var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
  padding: 34px;
  display: grid;
  gap: 16px;
}

.eyebrow {
  color: var(--pm-primary);
  letter-spacing: 0.16em;
  font-size: 11px;
  font-weight: 800;
}

.hero-copy h1 {
  margin-top: 8px;
  font-size: clamp(28px, 4vw, 46px);
  line-height: 1.08;
  color: var(--pm-text);
}

.hero-copy p {
  margin-top: 12px;
  max-width: 760px;
  color: var(--pm-text-soft);
  line-height: 1.75;
  font-size: 15px;
}

.hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hero-badges span {
  border: 1px solid #c8ddf0;
  border-radius: 999px;
  background: #edf7ff;
  color: #2b5379;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 700;
}

.manager-shell {
  margin-top: 14px;
}

@media (max-width: 760px) {
  .portfolio-view {
    padding: 16px 14px 40px;
  }

  .hero-banner {
    padding: 24px;
  }
}
</style>
