export const TRIAL_USAGE_LIMIT = 8
export const FREE_DAILY_USAGE_LIMIT = 20

export const PLAN_FEATURES = {
  trial: {
    title: '游客试用',
    description: `无需注册，累计可试用 ${TRIAL_USAGE_LIMIT} 次核心功能`,
  },
  free: {
    title: 'Free',
    description: `注册后每日可免费使用 ${FREE_DAILY_USAGE_LIMIT} 次（AI 调整/导出）`,
  },
  pro: {
    title: 'Pro',
    description: '无限次使用 AI 调整与导出，适合商业生产与团队协作场景',
  },
}
