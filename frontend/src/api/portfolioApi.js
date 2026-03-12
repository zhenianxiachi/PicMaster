import axios from 'axios'
import config from '../config'
import { errorHandler } from '../utils/errorHandler'

const apiClient = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use(requestConfig => {
  try {
    const rawSession = localStorage.getItem('picmaster_session_v2')
    if (rawSession) {
      const session = JSON.parse(rawSession)
      if (session?.token) {
        requestConfig.headers = requestConfig.headers || {}
        requestConfig.headers.Authorization = `Bearer ${session.token}`
      }
    }
  } catch {
    // no-op
  }
  return requestConfig
})

apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.code === 'ECONNABORTED') {
      errorHandler.handleNetworkError()
      return Promise.reject(error)
    }
    return Promise.reject(error)
  }
)

// 作品集相关API
export const portfolioApi = {
  getPortfolios: async () => {
    try {
      const response = await apiClient.get('/portfolios/')
      return response.data.portfolios
    } catch (error) {
      errorHandler.handleApiError(error, '获取作品集列表失败')
      throw error
    }
  },
  
  getPortfolioDetail: async (portfolioId) => {
    try {
      const response = await apiClient.get(`/portfolios/${portfolioId}`)
      return response.data.portfolio
    } catch (error) {
      errorHandler.handleApiError(error, '获取作品集详情失败')
      throw error
    }
  },
  
  createPortfolio: async (portfolioData) => {
    try {
      const response = await apiClient.post('/portfolios/', portfolioData)
      return response.data.portfolio
    } catch (error) {
      errorHandler.handleApiError(error, '创建作品集失败')
      throw error
    }
  },
  
  updatePortfolio: async (portfolioId, portfolioData) => {
    try {
      const response = await apiClient.put(`/portfolios/${portfolioId}`, portfolioData)
      return response.data.portfolio
    } catch (error) {
      errorHandler.handleApiError(error, '更新作品集失败')
      throw error
    }
  },
  
  deletePortfolio: async (portfolioId) => {
    try {
      const response = await apiClient.delete(`/portfolios/${portfolioId}`)
      return response.data
    } catch (error) {
      errorHandler.handleApiError(error, '删除作品集失败')
      throw error
    }
  },
  
  getCategories: async () => {
    try {
      const response = await apiClient.get('/portfolios/categories')
      return response.data.categories
    } catch (error) {
      errorHandler.handleApiError(error, '获取分类列表失败')
      throw error
    }
  },
  
  getTags: async () => {
    try {
      const response = await apiClient.get('/portfolios/tags')
      return response.data.tags
    } catch (error) {
      errorHandler.handleApiError(error, '获取标签列表失败')
      throw error
    }
  },
  
  uploadImageToPortfolio: async (portfolioId, formData) => {
    try {
      formData.append('portfolio_id', portfolioId)
      const response = await apiClient.post('/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      errorHandler.handleApiError(error, '上传图片失败')
      throw error
    }
  }
}

// 图片相关API
export const imageApi = {
  // 删除图片
  deleteImage: async (imageId) => {
    try {
      const response = await apiClient.delete(`/images/${imageId}`)
      return response.data
    } catch (error) {
      console.error('删除图片失败:', error)
      throw error
    }
  },
  
  // 重新排序图片
  reorderImages: async (portfolioId, imageOrders) => {
    try {
      // 提取imageOrders中的id列表
      const imageIds = imageOrders.map(order => order.id)
      const response = await apiClient.put('/images/sort', {
        image_ids: imageIds
      })
      return response.data
    } catch (error) {
      console.error('重新排序图片失败:', error)
      throw error
    }
  }
}
