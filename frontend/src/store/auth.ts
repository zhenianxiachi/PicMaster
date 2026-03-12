import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export type UserPlan = 'FREE' | 'PRO'

export interface User {
  id: string
  username: string
  email: string
  role: 'user' | 'admin'
  plan: UserPlan
  createdAt: string
  lastLoginAt: string
}

interface UserAccount extends User {
  password: string
}

interface AuthSession {
  userId: string
  token: string
}

export interface LoginParams {
  identity: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
}

export interface AuthActionResult {
  success: boolean
  message: string
}

const ACCOUNTS_STORAGE_KEY = 'picmaster_accounts_v2'
const SESSION_STORAGE_KEY = 'picmaster_session_v2'

const readStorage = <T>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) {
      return fallback
    }
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

const writeStorage = (key: string, value: unknown): void => {
  localStorage.setItem(key, JSON.stringify(value))
}

const createId = (): string => {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const sanitizeAccount = (account: UserAccount): User => ({
  id: account.id,
  username: account.username,
  email: account.email,
  role: account.role,
  plan: account.plan,
  createdAt: account.createdAt,
  lastLoginAt: account.lastLoginAt,
})

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const authDialogVisible = ref(false)
  const authDialogMode = ref<'login' | 'register'>('login')

  const isLoggedIn = computed(() => Boolean(user.value && token.value))
  const userRole = computed(() => user.value?.role ?? 'guest')
  const isPro = computed(() => user.value?.plan === 'PRO')
  const planLabel = computed(() => (isPro.value ? 'Pro' : 'Free'))

  const getAccounts = (): UserAccount[] => {
    return readStorage<UserAccount[]>(ACCOUNTS_STORAGE_KEY, [])
  }

  const saveAccounts = (accounts: UserAccount[]): void => {
    writeStorage(ACCOUNTS_STORAGE_KEY, accounts)
  }

  const persistSession = (nextSession: AuthSession | null): void => {
    if (!nextSession) {
      localStorage.removeItem(SESSION_STORAGE_KEY)
      return
    }
    writeStorage(SESSION_STORAGE_KEY, nextSession)
  }

  const setUser = (nextUser: User | null): void => {
    user.value = nextUser
    if (nextUser && token.value) {
      persistSession({ userId: nextUser.id, token: token.value })
    } else if (!nextUser) {
      persistSession(null)
    }
  }

  const setToken = (nextToken: string | null): void => {
    token.value = nextToken
    if (nextToken && user.value) {
      persistSession({ userId: user.value.id, token: nextToken })
    } else if (!nextToken) {
      persistSession(null)
    }
  }

  const getToken = (): string | null => token.value

  const openAuthDialog = (mode: 'login' | 'register' = 'login'): void => {
    authDialogMode.value = mode
    authDialogVisible.value = true
  }

  const closeAuthDialog = (): void => {
    authDialogVisible.value = false
  }

  const login = async (credentials: LoginParams): Promise<AuthActionResult> => {
    isLoading.value = true
    try {
      const identity = credentials.identity.trim().toLowerCase()
      const accounts = getAccounts()
      const account = accounts.find(
        item => item.email.toLowerCase() === identity || item.username.toLowerCase() === identity
      )

      if (!account || account.password !== credentials.password) {
        return { success: false, message: '账号或密码不正确' }
      }

      account.lastLoginAt = new Date().toISOString()
      saveAccounts(accounts)

      setUser(sanitizeAccount(account))
      setToken(createId())
      return { success: true, message: '登录成功' }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (payload: RegisterParams): Promise<AuthActionResult> => {
    isLoading.value = true
    try {
      const username = payload.username.trim()
      const email = payload.email.trim().toLowerCase()

      if (!username || !email || !payload.password) {
        return { success: false, message: '请完整填写注册信息' }
      }

      const accounts = getAccounts()
      const hasDuplicate = accounts.some(
        item => item.username.toLowerCase() === username.toLowerCase() || item.email.toLowerCase() === email
      )

      if (hasDuplicate) {
        return { success: false, message: '用户名或邮箱已存在' }
      }

      const now = new Date().toISOString()
      const account: UserAccount = {
        id: createId(),
        username,
        email,
        password: payload.password,
        role: 'user',
        plan: 'FREE',
        createdAt: now,
        lastLoginAt: now,
      }

      accounts.push(account)
      saveAccounts(accounts)

      setUser(sanitizeAccount(account))
      setToken(createId())
      return { success: true, message: '注册成功，欢迎使用 PicMaster' }
    } finally {
      isLoading.value = false
    }
  }

  const logout = (): void => {
    setUser(null)
    setToken(null)
  }

  const refreshUserInfo = async (): Promise<boolean> => {
    const session = readStorage<AuthSession | null>(SESSION_STORAGE_KEY, null)
    if (!session?.userId) {
      logout()
      return false
    }

    const account = getAccounts().find(item => item.id === session.userId)
    if (!account) {
      logout()
      return false
    }

    setUser(sanitizeAccount(account))
    setToken(session.token)
    return true
  }

  const initializeAuth = (): void => {
    const session = readStorage<AuthSession | null>(SESSION_STORAGE_KEY, null)
    if (!session?.userId || !session.token) {
      logout()
      return
    }

    const account = getAccounts().find(item => item.id === session.userId)
    if (!account) {
      logout()
      return
    }

    setUser(sanitizeAccount(account))
    setToken(session.token)
  }

  const upgradeToPro = (): boolean => {
    if (!user.value) {
      return false
    }

    const accounts = getAccounts()
    const account = accounts.find(item => item.id === user.value?.id)
    if (!account) {
      return false
    }

    account.plan = 'PRO'
    account.lastLoginAt = new Date().toISOString()
    saveAccounts(accounts)
    setUser(sanitizeAccount(account))
    return true
  }

  return {
    user,
    token,
    isLoading,
    authDialogVisible,
    authDialogMode,
    isLoggedIn,
    userRole,
    isPro,
    planLabel,
    setUser,
    setToken,
    getToken,
    openAuthDialog,
    closeAuthDialog,
    login,
    register,
    logout,
    refreshUserInfo,
    initializeAuth,
    upgradeToPro,
  }
})
