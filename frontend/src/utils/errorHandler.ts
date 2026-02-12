import { ElMessage } from 'element-plus'
import { logger } from './logger'

export interface ApiError {
  message: string
  status?: number
  code?: string
}

export const errorHandler = {
  handleApiError: (error: any, defaultMessage: string = '操作失败，请重试') => {
    logger.error('API Error:', error)
    
    let message = defaultMessage
    
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      if (status === 401) {
        message = '未授权，请重新登录'
      } else if (status === 403) {
        message = '没有权限执行此操作'
      } else if (status === 404) {
        message = '请求的资源不存在'
      } else if (status === 500) {
        message = '服务器错误，请稍后重试'
      } else if (data && data.error) {
        message = data.error
      }
    } else if (error.message) {
      message = error.message
    }
    
    ElMessage.error(message)
    return message
  },
  
  handleNetworkError: () => {
    logger.error('Network Error')
    ElMessage.error('网络连接失败，请检查网络设置')
  },
  
  handleValidationError: (errors: Record<string, string[]>) => {
    const messages = Object.values(errors).flat()
    if (messages.length > 0) {
      ElMessage.error(messages[0])
    }
  }
}
