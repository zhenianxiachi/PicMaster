import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { FREE_DAILY_USAGE_LIMIT, TRIAL_USAGE_LIMIT } from '@/config/businessRules'
import { useAuthStore } from '@/store/auth'

type LimitReason = 'trial' | 'daily'

export type UsageFeature = 'ai-adjust' | 'export-image' | 'save-portfolio'

interface UsageRecord {
  trialUsed: number
  dailyUsed: number
  dailyDate: string
}

type UsageLedger = Record<string, UsageRecord>

const STORAGE_KEY = 'picmaster_usage_v2'
const GUEST_KEY = 'guest'

const readLedger = (): UsageLedger => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return {}
    }
    return JSON.parse(raw) as UsageLedger
  } catch {
    return {}
  }
}

const writeLedger = (ledger: UsageLedger): void => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ledger))
}

const getDateKey = (): string => {
  const now = new Date()
  const year = now.getFullYear()
  const month = `${now.getMonth() + 1}`.padStart(2, '0')
  const day = `${now.getDate()}`.padStart(2, '0')
  return `${year}-${month}-${day}`
}

const createRecord = (): UsageRecord => ({
  trialUsed: 0,
  dailyUsed: 0,
  dailyDate: getDateKey(),
})

export const useUsageStore = defineStore('usage', () => {
  const authStore = useAuthStore()
  const usageLedger = ref<UsageLedger>(readLedger())
  const upgradeDialogVisible = ref(false)
  const upgradeReason = ref<LimitReason>('daily')
  const blockedFeature = ref<UsageFeature>('export-image')

  const recordKey = computed(() => authStore.user?.id ?? GUEST_KEY)

  const ensureRecord = (key: string): UsageRecord => {
    if (!usageLedger.value[key]) {
      usageLedger.value[key] = createRecord()
    }
    return usageLedger.value[key]
  }

  const normalizeDailyUsage = (record: UsageRecord): void => {
    const today = getDateKey()
    if (record.dailyDate === today) {
      return
    }
    record.dailyDate = today
    record.dailyUsed = 0
  }

  const persist = (): void => {
    writeLedger(usageLedger.value)
  }

  const initializeUsage = (): void => {
    usageLedger.value = readLedger()
    ensureRecord(GUEST_KEY)
    ensureRecord(recordKey.value)
    normalizeDailyUsage(ensureRecord(recordKey.value))
    persist()
  }

  const currentUsageRecord = computed(() => {
    const record = ensureRecord(recordKey.value)
    normalizeDailyUsage(record)
    return record
  })

  const guestRecord = computed(() => ensureRecord(GUEST_KEY))
  const trialUsed = computed(() => guestRecord.value.trialUsed)
  const dailyUsed = computed(() => currentUsageRecord.value.dailyUsed)
  const trialRemaining = computed(() => Math.max(0, TRIAL_USAGE_LIMIT - trialUsed.value))

  const dailyRemaining = computed(() => {
    if (!authStore.isLoggedIn || authStore.isPro) {
      return FREE_DAILY_USAGE_LIMIT
    }
    return Math.max(0, FREE_DAILY_USAGE_LIMIT - dailyUsed.value)
  })

  const activeLimit = computed(() => (authStore.isLoggedIn ? FREE_DAILY_USAGE_LIMIT : TRIAL_USAGE_LIMIT))
  const activeUsed = computed(() => (authStore.isLoggedIn ? dailyUsed.value : trialUsed.value))
  const usagePercent = computed(() => {
    if (authStore.isPro) {
      return 0
    }
    return Math.min(100, Math.round((activeUsed.value / activeLimit.value) * 100))
  })

  const usageSummary = computed(() => {
    if (authStore.isPro) {
      return {
        label: 'Pro 无限使用',
        detail: 'AI 调整与导出不受限',
      }
    }

    if (authStore.isLoggedIn) {
      return {
        label: `今日免费剩余 ${dailyRemaining.value}/${FREE_DAILY_USAGE_LIMIT}`,
        detail: `每日可用 ${FREE_DAILY_USAGE_LIMIT} 次`,
      }
    }

    return {
      label: `试用剩余 ${trialRemaining.value}/${TRIAL_USAGE_LIMIT}`,
      detail: `游客总试用 ${TRIAL_USAGE_LIMIT} 次`,
    }
  })

  const openUpgradeDialog = (reason: LimitReason, feature: UsageFeature = 'export-image'): void => {
    upgradeReason.value = reason
    blockedFeature.value = feature
    upgradeDialogVisible.value = true
  }

  const closeUpgradeDialog = (): void => {
    upgradeDialogVisible.value = false
  }

  const consume = (feature: UsageFeature): boolean => {
    if (authStore.isPro) {
      return true
    }

    if (!authStore.isLoggedIn) {
      const record = ensureRecord(GUEST_KEY)
      if (record.trialUsed >= TRIAL_USAGE_LIMIT) {
        openUpgradeDialog('trial', feature)
        return false
      }
      record.trialUsed += 1
      persist()
      return true
    }

    const record = currentUsageRecord.value
    if (record.dailyUsed >= FREE_DAILY_USAGE_LIMIT) {
      openUpgradeDialog('daily', feature)
      return false
    }

    record.dailyUsed += 1
    persist()
    return true
  }

  watch(
    () => authStore.user?.id,
    () => {
      ensureRecord(recordKey.value)
      normalizeDailyUsage(ensureRecord(recordKey.value))
      persist()
    },
    { immediate: true }
  )

  watch(
    () => authStore.user?.plan,
    plan => {
      if (plan === 'PRO') {
        closeUpgradeDialog()
      }
    }
  )

  return {
    trialLimit: TRIAL_USAGE_LIMIT,
    dailyLimit: FREE_DAILY_USAGE_LIMIT,
    usageSummary,
    trialUsed,
    dailyUsed,
    activeLimit,
    activeUsed,
    usagePercent,
    trialRemaining,
    dailyRemaining,
    upgradeDialogVisible,
    upgradeReason,
    blockedFeature,
    initializeUsage,
    openUpgradeDialog,
    closeUpgradeDialog,
    consume,
  }
})
