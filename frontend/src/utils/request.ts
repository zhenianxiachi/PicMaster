import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types'
// import { useAuthStore } from '@/store/auth'

/**
 * 创建axios实例
 */
const axiosInstance: AxiosInstance = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器
 */
axiosInstance.interceptors.request.use(config => {
  let token = ''
  try {
    const rawSession = localStorage.getItem('picmaster_session_v2')
    if (rawSession) {
      const parsed = JSON.parse(rawSession) as { token?: string }
      token = parsed.token || ''
    }
  } catch {
    token = ''
  }

  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }

  // 处理文件上传
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type']
  }

  return config
})

/**
 * 响应拦截器
 */
axiosInstance.interceptors.response.use(
  response => {
    // 跳过blob响应（文件下载）的处理
    if (response.data instanceof Blob) {
      return response
    }

    if (response.data) {
      if (response.data.code === 0) {
        if (response.data.message) {
          ElMessage.success(response.data.message)
        }
        return response
      } else {
        // 可以在这里添加全局错误处理，比如显示消息提示
        ElMessage.error(response.data.message)
      }
    }
    return response
  },
  error => {
    ElMessage.error('无法连接服务器')
    return Promise.reject(error)
  }
)

/**
 * 请求函数包装器，自动将返回类型包装为 Response<T>
 */
const request = <T = unknown>(
  config: AxiosRequestConfig
): Promise<AxiosResponse<ApiResponse<T>> & { success: boolean }> => {
  return axiosInstance<ApiResponse<T>>(config).then(res => {
    return { ...res, success: res.data.code === 0 }
  })
}

/**
 * 文件上传 - 不自动提取data字段
 */
export const uploadFile = (
  url: string,
  data: FormData
): Promise<AxiosResponse<ApiResponse<unknown>>> => {
  return axiosInstance.post<ApiResponse<unknown>>(url, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/**
 * 文件下载 - 返回原始response
 */
export const downloadFile = (url: string, params?: unknown): Promise<AxiosResponse<Blob>> => {
  return axiosInstance.get(url, {
    params,
    responseType: 'blob',
  })
}

export default request
