<template>
  <div class="editor-intro">
    <section class="intro-shell">
      <article class="intro-main">
        <p class="kicker">EDITOR CONSOLE</p>
        <h1>高品质图像编辑工作台</h1>
        <p>
          提供 AI 智能调色、手动参数精修、无损导出和作品集归档能力，覆盖商业摄影后期的完整流程。
        </p>
        <div class="intro-actions">
          <button class="btn-primary" @click="goToEditor">进入编辑器</button>
          <button class="btn-ghost" @click="goToPortfolio">进入作品集</button>
        </div>
      </article>

      <article class="intro-rules">
        <h3>运营规则</h3>
        <ul>
          <li>游客试用：{{ TRIAL_USAGE_LIMIT }} 次</li>
          <li>Free 账号：每日 {{ FREE_DAILY_USAGE_LIMIT }} 次</li>
          <li>超限后自动弹出升级引导</li>
        </ul>
        <div class="quota-label">{{ usageStore.usageSummary.label }}</div>
      </article>
    </section>

    <section class="quota-shell">
      <h2>当前额度状态</h2>
      <div class="quota-grid">
        <article class="quota-card">
          <span>当前消耗</span>
          <strong>{{ usageStore.activeUsed }} / {{ usageStore.activeLimit }}</strong>
          <el-progress :percentage="usageStore.usagePercent" :stroke-width="10" />
        </article>
        <article class="quota-card">
          <span>游客剩余</span>
          <strong>{{ usageStore.trialRemaining }} / {{ TRIAL_USAGE_LIMIT }}</strong>
          <el-progress :percentage="trialPercent" :stroke-width="10" color="#0f7ccf" />
        </article>
        <article class="quota-card">
          <span>今日免费剩余</span>
          <strong>{{ usageStore.dailyRemaining }} / {{ FREE_DAILY_USAGE_LIMIT }}</strong>
          <el-progress :percentage="dailyPercent" :stroke-width="10" color="#13b5a8" />
        </article>
      </div>
    </section>

    <section class="cap-grid">
      <article class="cap-card">13 项专业参数调节</article>
      <article class="cap-card">AI 意图解析与快速调色</article>
      <article class="cap-card">支持 PNG / JPEG 导出策略</article>
      <article class="cap-card">支持作品集同步与交付展示</article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { FREE_DAILY_USAGE_LIMIT, TRIAL_USAGE_LIMIT } from '@/config/businessRules'
import { useUsageStore } from '@/store/usage'

const router = useRouter()
const usageStore = useUsageStore()

const trialPercent = computed(() => Math.round((usageStore.trialRemaining / TRIAL_USAGE_LIMIT) * 100))
const dailyPercent = computed(() => Math.round((usageStore.dailyRemaining / FREE_DAILY_USAGE_LIMIT) * 100))

const goToEditor = (): void => {
  router.push('/editor')
}

const goToPortfolio = (): void => {
  router.push('/portfolio')
}
</script>

<style scoped>
.editor-intro {
  min-height: calc(100vh - 122px);
  padding: 26px 24px 52px;
}

.intro-shell,
.quota-shell,
.cap-grid {
  max-width: 1320px;
  margin: 0 auto;
}

.intro-shell {
  display: grid;
  grid-template-columns: 1.28fr 0.72fr;
  gap: 12px;
}

.intro-main,
.intro-rules {
  border: 1px solid var(--pm-border);
  border-radius: 20px;
  background: var(--pm-surface);
  box-shadow: var(--pm-shadow-1);
}

.intro-main {
  padding: 40px;
}

.kicker {
  color: var(--pm-primary);
  font-size: 11px;
  letter-spacing: 0.13em;
  font-weight: 800;
}

.intro-main h1 {
  margin-top: 12px;
  font-size: clamp(34px, 5vw, 54px);
  line-height: 1.08;
  letter-spacing: -0.03em;
  color: var(--pm-text);
}

.intro-main p {
  margin-top: 16px;
  max-width: 740px;
  color: var(--pm-text-soft);
  line-height: 1.75;
  font-size: 16px;
}

.intro-actions {
  margin-top: 28px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-ghost {
  height: 44px;
  border-radius: 999px;
  padding: 0 20px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  border: 0;
  color: #ffffff;
  background: linear-gradient(125deg, var(--pm-primary), #16a4cb);
}

.btn-ghost {
  border: 1px solid #bfd8ec;
  color: #1f4a73;
  background: #ecf7ff;
}

.intro-rules {
  padding: 24px;
  background:
    radial-gradient(circle at 100% 0%, rgba(19, 181, 168, 0.16), transparent 35%),
    var(--pm-surface);
}

.intro-rules h3 {
  font-size: 24px;
  color: var(--pm-text);
}

.intro-rules ul {
  margin-top: 12px;
  padding-left: 18px;
  color: #587291;
  line-height: 1.8;
}

.quota-label {
  margin-top: 16px;
  border: 1px solid #c8dff0;
  border-radius: 10px;
  background: #edf7ff;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 700;
  color: #23496f;
}

.quota-shell {
  margin-top: 12px;
  border: 1px solid var(--pm-border);
  border-radius: 20px;
  background: var(--pm-surface);
  padding: 22px;
}

.quota-shell h2 {
  font-size: 26px;
  color: var(--pm-text);
}

.quota-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.quota-card {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  background: #f7fbff;
  padding: 14px;
}

.quota-card span {
  font-size: 12px;
  color: #5f7793;
  font-weight: 700;
}

.quota-card strong {
  margin: 8px 0 10px;
  display: block;
  font-size: 26px;
  color: var(--pm-text);
  letter-spacing: -0.03em;
}

.cap-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.cap-card {
  border: 1px solid var(--pm-border);
  border-radius: 12px;
  background: var(--pm-surface);
  padding: 16px;
  color: #3c5f82;
  font-size: 13px;
  font-weight: 700;
}

@media (max-width: 980px) {
  .intro-shell {
    grid-template-columns: 1fr;
  }

  .quota-grid {
    grid-template-columns: 1fr;
  }

  .cap-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .editor-intro {
    padding: 16px 14px 36px;
  }

  .intro-main,
  .intro-rules,
  .quota-shell {
    padding: 20px;
  }

  .cap-grid {
    grid-template-columns: 1fr;
  }
}
</style>
