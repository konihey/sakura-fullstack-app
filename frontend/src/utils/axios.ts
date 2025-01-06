// src/utils/axios.ts
import axios, { AxiosError } from 'axios'
import { API_BASE_URL } from '@/constants/api'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json'
    }
  })
  
  apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
      console.log('Request URL:', config.url)
      console.log('Token being set:', token)
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${token}`
      console.log('Final headers:', config.headers)
    }
    return config
  })
  
  // レスポンスインターセプターを追加
  apiClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      if (error.response?.status === 401) {
        const authStore = useAuthStore()
        const router = useRouter()

        // ログアウト処理
        authStore.logout()
        
        // ユーザーに通知
        ElMessage.warning('セッションが切れました。再度ログインしてください。')
        
        // ログインページへリダイレクト
        router.push('/login')
        
      }
      return Promise.reject(error)
    }
  )
  
  export default apiClient