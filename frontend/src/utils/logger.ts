const isDevelopment = import.meta.env.DEV

export const logger = {
  log: (...args: any[]) => {
    if (isDevelopment) {
      console.log('[PicMaster]', ...args)
    }
  },
  
  error: (...args: any[]) => {
    console.error('[PicMaster Error]', ...args)
  },
  
  warn: (...args: any[]) => {
    if (isDevelopment) {
      console.warn('[PicMaster Warning]', ...args)
    }
  },
  
  info: (...args: any[]) => {
    if (isDevelopment) {
      console.info('[PicMaster Info]', ...args)
    }
  }
}
