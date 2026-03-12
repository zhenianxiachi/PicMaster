<template>
  <div class="home-view">
    <section class="hero">
      <div class="hero-left">
        <p class="kicker">COMMERCIAL IMAGE PLATFORM</p>
        <h1>更高级的在线图像编辑体验</h1>
        <p class="subtitle">
          从游客试用到 Pro 转化，PicMaster 提供完整运营闭环，兼顾美观界面、专业效率与商业化规则。
        </p>
        <div class="hero-actions">
          <button class="btn-primary" @click="goToEditor">开始编辑</button>
          <button class="btn-ghost" @click="goToViewer">查看展示页</button>
        </div>
      </div>

      <div class="hero-right">
        <div class="showcase-card large">
          <strong>运营规则</strong>
          <p>游客试用 {{ TRIAL_USAGE_LIMIT }} 次，注册后每日 {{ FREE_DAILY_USAGE_LIMIT }} 次。</p>
        </div>
        <div class="showcase-row">
          <div class="showcase-card">
            <strong>账号体系</strong>
            <p>登录、注册、会话恢复</p>
          </div>
          <div class="showcase-card">
            <strong>升级策略</strong>
            <p>超限触发升级引导</p>
          </div>
        </div>
      </div>
    </section>

    <section class="metrics">
      <article v-for="item in metrics" :key="item.label" class="metric-card">
        <div class="value">{{ item.value }}</div>
        <div class="label">{{ item.label }}</div>
        <p>{{ item.desc }}</p>
      </article>
    </section>

    <section class="feature-grid">
      <article class="feature-card">
        <h3>用户管理</h3>
        <p>支持登录注册、会话恢复和套餐状态同步。</p>
      </article>
      <article class="feature-card">
        <h3>配额控制</h3>
        <p>试用次数 + 每日免费额度双策略，防止无限制免费使用。</p>
      </article>
      <article class="feature-card">
        <h3>付费升级</h3>
        <p>在关键操作点触发升级弹窗，建立稳定转化入口。</p>
      </article>
      <article class="feature-card">
        <h3>高质界面</h3>
        <p>统一视觉系统，强调专业感、可信度和可读性。</p>
      </article>
    </section>

    <section class="plan-panel">
      <h2>套餐结构</h2>
      <div class="plans">
        <article class="plan">
          <span>{{ PLAN_FEATURES.trial.title }}</span>
          <strong>{{ TRIAL_USAGE_LIMIT }} 次</strong>
          <p>{{ PLAN_FEATURES.trial.description }}</p>
        </article>
        <article class="plan">
          <span>{{ PLAN_FEATURES.free.title }}</span>
          <strong>{{ FREE_DAILY_USAGE_LIMIT }} 次/天</strong>
          <p>{{ PLAN_FEATURES.free.description }}</p>
        </article>
        <article class="plan pro">
          <span>{{ PLAN_FEATURES.pro.title }}</span>
          <strong>无限制</strong>
          <p>{{ PLAN_FEATURES.pro.description }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { FREE_DAILY_USAGE_LIMIT, PLAN_FEATURES, TRIAL_USAGE_LIMIT } from '@/config/businessRules'

const router = useRouter()

const metrics = [
  { value: '4.8/5', label: '用户体验评分', desc: '编辑效率与视觉体验同时提升' },
  { value: '99.9%', label: '可用性目标', desc: '面向商业图像交付场景' },
  { value: '<3s', label: '常规导出耗时', desc: '常见图像尺寸下快速响应' },
  { value: '3 层', label: '运营漏斗', desc: '试用 → 免费 → Pro 的转化路径' },
]

const goToEditor = (): void => {
  router.push('/editor-intro')
}

const goToViewer = (): void => {
  router.push('/viewer')
}
</script>

<style scoped>
.home-view {
  min-height: calc(100vh - 122px);
  padding: 28px 24px 56px;
}

.hero,
.metrics,
.feature-grid,
.plan-panel {
  max-width: 1320px;
  margin: 0 auto;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
}

.hero-left,
.hero-right {
  border: 1px solid var(--pm-border);
  border-radius: var(--pm-radius-lg);
  background: var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
}

.hero-left {
  padding: 44px;
}

.kicker {
  color: var(--pm-primary);
  font-size: 11px;
  letter-spacing: 0.14em;
  font-weight: 800;
}

.hero-left h1 {
  margin-top: 14px;
  font-size: clamp(34px, 5vw, 58px);
  line-height: 1.06;
  letter-spacing: -0.03em;
  color: var(--pm-text);
}

.subtitle {
  margin-top: 16px;
  color: var(--pm-text-soft);
  line-height: 1.75;
  font-size: 17px;
  max-width: 680px;
}

.hero-actions {
  margin-top: 30px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-ghost {
  height: 46px;
  min-width: 150px;
  border-radius: 999px;
  padding: 0 22px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  border: 0;
  color: #ffffff;
  background: linear-gradient(125deg, var(--pm-primary), #17a4cf);
}

.btn-ghost {
  border: 1px solid #bfd8ec;
  color: #1f4a73;
  background: #ecf7ff;
}

.hero-right {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background:
    radial-gradient(circle at 0% 0%, rgba(19, 181, 168, 0.12), transparent 46%),
    var(--pm-surface);
}

.showcase-card {
  border: 1px solid #d3e3f2;
  border-radius: 14px;
  background: #f7fbff;
  padding: 16px;
}

.showcase-card.large {
  min-height: 156px;
}

.showcase-card strong {
  display: block;
  font-size: 20px;
  color: var(--pm-text);
}

.showcase-card p {
  margin-top: 8px;
  font-size: 13px;
  color: #5f7893;
  line-height: 1.65;
}

.showcase-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.metrics {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.metric-card {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: var(--pm-surface);
  padding: 18px;
}

.metric-card .value {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--pm-text);
}

.metric-card .label {
  margin-top: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #36587d;
}

.metric-card p {
  margin-top: 8px;
  font-size: 12px;
  color: #67819b;
  line-height: 1.55;
}

.feature-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.feature-card {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: var(--pm-surface);
  padding: 18px;
}

.feature-card h3 {
  font-size: 18px;
  color: var(--pm-text);
}

.feature-card p {
  margin-top: 8px;
  font-size: 13px;
  color: var(--pm-text-soft);
  line-height: 1.65;
}

.plan-panel {
  margin-top: 18px;
  border: 1px solid var(--pm-border);
  border-radius: 20px;
  background: var(--pm-surface);
  padding: 24px;
}

.plan-panel h2 {
  font-size: 28px;
  color: var(--pm-text);
}

.plans {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.plan {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  padding: 16px;
  background: #f7fbff;
}

.plan.pro {
  border-color: #efca86;
  background: linear-gradient(150deg, #fff8ea, #fff3d8);
}

.plan span {
  font-size: 12px;
  color: #5d758f;
  font-weight: 700;
}

.plan strong {
  display: block;
  margin-top: 8px;
  font-size: 30px;
  letter-spacing: -0.03em;
  color: var(--pm-text);
}

.plan p {
  margin-top: 10px;
  font-size: 13px;
  line-height: 1.6;
  color: #5d758f;
}

@media (max-width: 1120px) {
  .metrics,
  .feature-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 920px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .plans {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .home-view {
    padding: 18px 14px 40px;
  }

  .hero-left {
    padding: 26px;
  }

  .metrics,
  .feature-grid,
  .showcase-row {
    grid-template-columns: 1fr;
  }
}
</style>
