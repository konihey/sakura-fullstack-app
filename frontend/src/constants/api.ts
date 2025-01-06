// src/constants/api.ts
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost'

export const API_ENDPOINTS = {
  AUTH: {
    SIGN_UP: '/api/auth/sign-up',
    LOGIN: '/api/auth/login',
    ME: '/api/auth/me'
  },
  USERS: {
    LIST: '/api/users',
    DELETE: (id: number) => `/api/users/${id}`
  }
} as const

// API クライアントの設定は既にベースURLを使用しているはずなので
// src/utils/axios.ts で
// const apiClient = axios.create({ baseURL: API_BASE_URL })
// のように設定されていれば、パスだけの指定で OK