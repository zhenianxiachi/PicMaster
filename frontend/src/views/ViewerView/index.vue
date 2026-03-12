<template>
  <div class="viewer-view">
    <section class="hero-banner">
      <div class="hero-copy">
        <p class="eyebrow">DELIVERY EXPERIENCE</p>
        <h1>作品展示与客户预览</h1>
        <p>
          用高质量展示界面交付作品，支持二维码分享、全屏预览与 AI 快速调色，提升客户感知与成片价值。
        </p>
      </div>
      <div class="hero-badges">
        <span>Live Preview</span>
        <span>AI Assistant</span>
        <span>QR Sharing</span>
      </div>
    </section>

    <section class="viewer-shell">
      <PortfolioViewer :initial-portfolio-id="initialPortfolioId" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import PortfolioViewer from '@/components/PortfolioViewer.vue'

const initialPortfolioId = ref<number | null>(null)

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const rawPortfolioId = urlParams.get('portfolio_id')

  if (!rawPortfolioId) {
    initialPortfolioId.value = null
    return
  }

  const parsed = Number.parseInt(rawPortfolioId, 10)
  initialPortfolioId.value = Number.isNaN(parsed) ? null : parsed
})
</script>

<style scoped>
.viewer-view {
  min-height: calc(100vh - 122px);
  padding: 22px 24px 56px;
}

.hero-banner,
.viewer-shell {
  max-width: 1320px;
  margin: 0 auto;
}

.hero-banner {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-lg);
  background:
    radial-gradient(circle at 10% 0%, rgba(15, 124, 207, 0.14), transparent 42%),
    radial-gradient(circle at 100% 100%, rgba(243, 166, 68, 0.16), transparent 38%),
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
  border: 1px solid #d5c48f;
  border-radius: 999px;
  background: #fff6e3;
  color: #75520b;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 700;
}

.viewer-shell {
  margin-top: 14px;
}

@media (max-width: 760px) {
  .viewer-view {
    padding: 16px 14px 40px;
  }

  .hero-banner {
    padding: 24px;
  }
}
</style>
