/**
 * 图片类型定义
 */
export interface Image {
  id: string
  url: string
  name: string
  thumbnail?: string
  width?: number
  height?: number
  size?: number
  type?: string
  createdAt?: string
  updatedAt?: string
}

/**
 * 滤镜类型定义
 */
export interface Filter {
  id: string
  name: string
  type: string
  params: Record<string, any>
  preview?: string
}

/**
 * 标注类型定义
 */
export interface Annotation {
  id: string
  type: 'text' | 'arrow' | 'rect' | 'circle'
  x: number
  y: number
  width?: number
  height?: number
  content?: string
  color?: string
  fontSize?: number
  createdAt: string
  updatedAt?: string
}

/**
 * 作品集类型定义
 */
export interface Portfolio {
  id: string
  title: string
  description?: string
  images: Image[]
  thumbnail?: string
  createdAt: string
  updatedAt?: string
}

/**
 * 作品集创建参数
 */
export interface CreatePortfolioParams {
  title: string
  description?: string
  images: Image[]
}

/**
 * 作品集更新参数
 */
export interface UpdatePortfolioParams {
  id: string
  title?: string
  description?: string
  images?: Image[]
}

/**
 * API 响应基础类型
 */
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}
