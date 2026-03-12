import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User, type UsageToday } from '../api/authApi'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)
  const usageToday = ref<UsageToday | null>(null)

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isPremium = computed(() => user.value?.membership_type === 'premium' || user.value?.membership_type === 'pro')

  const login = async (username: string, password: string) => {
    const response = await authApi.login(username, password)
    token.value = response.token
    user.value = response.user
    localStorage.setItem('token', response.token)
    return response
  }

  const register = async (username: string, email: string, password: string) => {
    const response = await authApi.register(username, email, password)
    token.value = response.token
    user.value = response.user
    localStorage.setItem('token', response.token)
    return response
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      usageToday.value = null
      localStorage.removeItem('token')
    }
  }

  const fetchProfile = async () => {
    if (!token.value) return
    try {
      const response = await authApi.getProfile()
      user.value = response.user
      usageToday.value = response.usage_today
    } catch (error) {
      console.error('Fetch profile error:', error)
      logout()
    }
  }

  const checkLimit = async (actionType: 'edit' | 'save' | 'export') => {
    if (!token.value) return { allowed: false, message: '请先登录', limit: 0, used: 0, remaining: 0 }
    try {
      return await authApi.checkLimit(actionType)
    } catch (error) {
      console.error('Check limit error:', error)
      return { allowed: false, message: '检查限制失败', limit: 0, used: 0, remaining: 0 }
    }
  }

  const recordUsage = async (actionType: 'edit' | 'save' | 'export') => {
    if (!token.value) return
    try {
      await authApi.recordUsage(actionType)
      if (usageToday.value) {
        if (actionType === 'edit') usageToday.value.edit_count++
        else if (actionType === 'save') usageToday.value.save_count++
        else if (actionType === 'export') usageToday.value.export_count++
      }
    } catch (error) {
      console.error('Record usage error:', error)
    }
  }

  const getRemainingCount = (actionType: 'edit' | 'save' | 'export') => {
    if (!user.value || !usageToday.value) return 0
    const limitKey = `daily_${actionType}_limit` as keyof User
    const countKey = `${actionType}_count` as keyof UsageToday
    const limit = user.value[limitKey] as number
    const used = usageToday.value[countKey] as number
    return Math.max(0, limit - used)
  }

  if (token.value) {
    fetchProfile()
  }

  return {
    token,
    user,
    usageToday,
    isLoggedIn,
    isPremium,
    login,
    register,
    logout,
    fetchProfile,
    checkLimit,
    recordUsage,
    getRemainingCount
  }
})
