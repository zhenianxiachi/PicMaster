<template>
  <el-dialog v-model="visible" width="620px" class="upgrade-dialog">
    <template #header>
      <div class="upgrade-header">
        <p class="kicker">PLAN UPGRADE</p>
        <h3>{{ title }}</h3>
        <p>{{ subtitle }}</p>
      </div>
    </template>

    <div class="plan-grid">
      <article class="plan-card">
        <h4>游客试用</h4>
        <strong>{{ trialLimit }} 次</strong>
        <p>无需登录即可体验核心流程。</p>
      </article>
      <article class="plan-card">
        <h4>Free</h4>
        <strong>{{ dailyLimit }} 次/天</strong>
        <p>注册后获得每日免费 AI 调整与导出额度。</p>
      </article>
      <article class="plan-card pro">
        <h4>Pro</h4>
        <strong>无限制</strong>
        <p>适配商业交付、持续生产与团队协作。</p>
      </article>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="usageStore.closeUpgradeDialog">稍后再说</el-button>
        <el-button v-if="!authStore.isLoggedIn" type="primary" @click="openRegister">注册获取免费额度</el-button>
        <el-button v-else-if="!authStore.isPro" type="warning" @click="upgradeNow">升级到 Pro（演示）</el-button>
        <el-button v-else type="primary" @click="usageStore.closeUpgradeDialog">我知道了</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { useUsageStore } from '@/store/usage'

const authStore = useAuthStore()
const usageStore = useUsageStore()

const visible = computed({
  get: () => usageStore.upgradeDialogVisible,
  set: value => {
    if (!value) {
      usageStore.closeUpgradeDialog()
    }
  },
})

const title = computed(() => (usageStore.upgradeReason === 'trial' ? '试用次数已用尽' : '今日免费额度已用尽'))

const subtitle = computed(() => {
  if (usageStore.upgradeReason === 'trial') {
    return '注册后可切换到每日免费额度，继续使用编辑能力。'
  }
  return '升级 Pro 可解除每日限制，保障持续商业化生产。'
})

const trialLimit = computed(() => usageStore.trialLimit)
const dailyLimit = computed(() => usageStore.dailyLimit)

const openRegister = (): void => {
  usageStore.closeUpgradeDialog()
  authStore.openAuthDialog('register')
}

const upgradeNow = (): void => {
  const upgraded = authStore.upgradeToPro()
  if (!upgraded) {
    ElMessage.error('升级失败，请重新登录后再试')
    return
  }
  usageStore.closeUpgradeDialog()
  ElMessage.success('已升级到 Pro，当前账号不限次数')
}
</script>

<style scoped>
.upgrade-header .kicker {
  color: var(--pm-primary);
  font-size: 11px;
  letter-spacing: 0.12em;
  font-weight: 800;
}

.upgrade-header h3 {
  margin-top: 8px;
  font-size: 30px;
  color: var(--pm-text);
  letter-spacing: -0.02em;
}

.upgrade-header p {
  margin-top: 8px;
  font-size: 13px;
  color: var(--pm-text-soft);
}

.plan-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.plan-card {
  border: 1px solid var(--pm-border);
  border-radius: 14px;
  padding: 18px 14px;
  background: #f7fbff;
}

.plan-card h4 {
  color: #3f5f7f;
  font-size: 13px;
  font-weight: 700;
}

.plan-card strong {
  margin-top: 8px;
  display: block;
  font-size: 28px;
  letter-spacing: -0.03em;
  color: var(--pm-text);
}

.plan-card p {
  margin-top: 8px;
  color: #62809f;
  font-size: 12px;
  line-height: 1.5;
}

.plan-card.pro {
  border-color: #efca86;
  background: linear-gradient(150deg, #fff8ea, #fff3d8);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .plan-grid {
    grid-template-columns: 1fr;
  }
}
</style>
