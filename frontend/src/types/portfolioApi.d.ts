declare module '@/api/portfolioApi.js' {
  export interface Portfolio {
    id: number
    name: string
    client_name: string
    shoot_date: string
    cover_image: string | null
    category_id: number | null
    user_id: number
    tags: number[]
    images: Image[]
    created_at: string
    updated_at: string
    image_count?: number
  }

  export interface Image {
    id: number
    filename: string
    filepath: string
    thumbnail_path: string
    sort_order: number
  }

  export interface Category {
    id: number
    name: string
  }

  export interface Tag {
    id: number
    name: string
  }

  export const portfolioApi: {
    getPortfolios: () => Promise<Portfolio[]>
    getPortfolioDetail: (portfolioId: number) => Promise<Portfolio>
    createPortfolio: (portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    updatePortfolio: (portfolioId: number, portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    deletePortfolio: (portfolioId: number) => Promise<{ message: string }>
    getCategories: () => Promise<Category[]>
    getTags: () => Promise<Tag[]>
    uploadImageToPortfolio: (portfolioId: number, formData: FormData) => Promise<{ message: string; images: Image[] }>
  }
}

declare module '../api/portfolioApi.js' {
  export interface Portfolio {
    id: number
    name: string
    client_name: string
    shoot_date: string
    cover_image: string | null
    category_id: number | null
    user_id: number
    tags: number[]
    images: Image[]
    created_at: string
    updated_at: string
    image_count?: number
  }

  export interface Image {
    id: number
    filename: string
    filepath: string
    thumbnail_path: string
    sort_order: number
  }

  export interface Category {
    id: number
    name: string
  }

  export interface Tag {
    id: number
    name: string
  }

  export const portfolioApi: {
    getPortfolios: () => Promise<Portfolio[]>
    getPortfolioDetail: (portfolioId: number) => Promise<Portfolio>
    createPortfolio: (portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    updatePortfolio: (portfolioId: number, portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    deletePortfolio: (portfolioId: number) => Promise<{ message: string }>
    getCategories: () => Promise<Category[]>
    getTags: () => Promise<Tag[]>
    uploadImageToPortfolio: (portfolioId: number, formData: FormData) => Promise<{ message: string; images: Image[] }>
  }
}

declare module '../../api/portfolioApi.js' {
  export interface Portfolio {
    id: number
    name: string
    client_name: string
    shoot_date: string
    cover_image: string | null
    category_id: number | null
    user_id: number
    tags: number[]
    images: Image[]
    created_at: string
    updated_at: string
    image_count?: number
  }

  export interface Image {
    id: number
    filename: string
    filepath: string
    thumbnail_path: string
    sort_order: number
  }

  export interface Category {
    id: number
    name: string
  }

  export interface Tag {
    id: number
    name: string
  }

  export const portfolioApi: {
    getPortfolios: () => Promise<Portfolio[]>
    getPortfolioDetail: (portfolioId: number) => Promise<Portfolio>
    createPortfolio: (portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    updatePortfolio: (portfolioId: number, portfolioData: Partial<Portfolio>) => Promise<Portfolio>
    deletePortfolio: (portfolioId: number) => Promise<{ message: string }>
    getCategories: () => Promise<Category[]>
    getTags: () => Promise<Tag[]>
    uploadImageToPortfolio: (portfolioId: number, formData: FormData) => Promise<{ message: string; images: Image[] }>
  }
}
