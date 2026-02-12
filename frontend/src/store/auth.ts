import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 用户信息接口
 */
export interface User {
  id: string
  username: string
  email: string
  avatar?: string
  role: string
  createdAt: string
}

/**
 * 登录请求参数接口
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 注册请求参数接口
 */
export interface RegisterParams {
  username: string
  email: string
  password: string
}

/**
 * 认证状态管理
 */
export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role || 'guest')

  // 方法

  /**
   * 设置用户信息
   * @param userData 用户数据
   */
  const setUser = (userData: User | null): void => {
    user.value = userData
  }

  /**
   * 设置认证令牌
   * @param authToken 认证令牌
   */
  const setToken = (authToken: string | null): void => {
    token.value = authToken
    if (authToken) {
      localStorage.setItem('auth_token', authToken)
    } else {
      localStorage.removeItem('auth_token')
    }
  }

  /**
   * 获取认证令牌
   * @returns 认证令牌
   */
  const getToken = (): string | null => {
    if (!token.value) {
      const savedToken = localStorage.getItem('auth_token')
      if (savedToken) {
        token.value = savedToken
      }
    }
    return token.value
  }

  /**
   * 登录
   * @param credentials 登录凭据
   * @returns Promise<boolean> 登录是否成功
   */
  const login = async (credentials: LoginParams): Promise<boolean> => {
    isLoading.value = true
    try {
      // TODO: 实现实际的登录 API 调用
      // const response = await request.post('/auth/login', credentials)

      // 模拟登录成功
      const mockUser: User = {
        id: '1',
        username: credentials.username,
        email: 'user@example.com',
        role: 'user',
        createdAt: new Date().toISOString(),
      }

      const mockToken = 'mock_jwt_token_' + Date.now()

      setUser(mockUser)
      setToken(mockToken)

      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 注册
   * @param userData 注册数据
   * @returns Promise<boolean> 注册是否成功
   */
  const register = async (userData: RegisterParams): Promise<boolean> => {
    isLoading.value = true
    try {
      // TODO: 实现实际的注册 API 调用
      // const response = await request.post('/auth/register', userData)

      return true
    } catch (error) {
      console.error('注册失败:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 登出
   */
  const logout = (): void => {
    setUser(null)
    setToken(null)
    // TODO: 清除其他相关数据
  }

  /**
   * 刷新用户信息
   * @returns Promise<boolean> 刷新是否成功
   */
  const refreshUserInfo = async (): Promise<boolean> => {
    const currentToken = getToken()
    if (!currentToken) {
      return false
    }

    isLoading.value = true
    try {
      // TODO: 实现获取用户信息的 API 调用
      // const response = await request.get('/auth/user')
      // setUser(response.data)

      return true
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      logout()
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 初始化认证状态
   */
  const initializeAuth = (): void => {
    const savedToken = localStorage.getItem('auth_token')
    if (savedToken) {
      token.value = savedToken
      refreshUserInfo()
    }
  }

  return {
    // 状态
    user,
    token,
    isLoading,

    // 计算属性
    isLoggedIn,
    userRole,

    // 方法
    setUser,
    setToken,
    getToken,
    login,
    register,
    logout,
    refreshUserInfo,
    initializeAuth,
  }
})
