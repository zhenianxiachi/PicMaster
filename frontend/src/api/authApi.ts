import axios from './index'

export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  membership_type: string
  daily_edit_limit: number
  daily_save_limit: number
  daily_export_limit: number
  created_at?: string
}

export interface UsageToday {
  edit_count: number
  save_count: number
  export_count: number
}

export interface AuthResponse {
  message: string
  token: string
  user: User
}

export interface LimitCheckResponse {
  allowed: boolean
  message?: string
  limit: number
  used: number
  remaining: number
}

export const authApi = {
  register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post('/auth/register', { username, email, password })
    return response.data
  },

  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post('/auth/login', { username, password })
    return response.data
  },

  getProfile: async (): Promise<{ user: User; usage_today: UsageToday }> => {
    const response = await axios.get('/auth/profile')
    return response.data
  },

  checkLimit: async (actionType: 'edit' | 'save' | 'export'): Promise<LimitCheckResponse> => {
    const response = await axios.post('/auth/check-limit', { action_type: actionType })
    return response.data
  },

  recordUsage: async (actionType: 'edit' | 'save' | 'export'): Promise<{ message: string; action_type: string; count: number }> => {
    const response = await axios.post('/auth/record-usage', { action_type: actionType })
    return response.data
  },

  logout: async (): Promise<{ message: string }> => {
    const response = await axios.post('/auth/logout')
    return response.data
  }
}
