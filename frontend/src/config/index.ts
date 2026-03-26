const browserHostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost'
const browserOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'
const envApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()
const envFrontendUrl = import.meta.env.VITE_FRONTEND_URL?.trim()
const defaultApiBaseUrl = `http://${browserHostname}:5000/api`

const config = {
  // In dev we follow the current page host so localhost and LAN access both work
  // without editing .env every time the machine IP changes.
  apiBaseUrl: import.meta.env.DEV ? defaultApiBaseUrl : envApiBaseUrl || defaultApiBaseUrl,
  frontendUrl: import.meta.env.DEV ? browserOrigin : envFrontendUrl || browserOrigin,
}

export default config
