// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AxiosError } from 'axios'

import { API_ENDPOINTS } from '@/constants/api'
import apiClient from '@/utils/axios'
import { handleApiError } from '@/utils/error-handler'
import type { User } from '@/types/user'
import type { LoginForm, RegisterForm } from '@/types/auth'
import type { ApiError } from '@/types/error'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const initialized = ref(false)
  const isAuthenticated = computed(() => !!token.value)
  
  const initialize = async () => {
    try {
      const savedToken = localStorage.getItem('token')
      if (savedToken) {
        token.value = savedToken
        await fetchCurrentUser()
      }
    } catch (error) {
      console.error('Initialization failed:', error)
      logout()
    } finally {
      initialized.value = true
    }
  }
  
  const login = async (credentials: LoginForm) => {
    try {
      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials)
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      user.value = response.data.user
      return true
    } catch (error) {
      handleApiError(error as AxiosError<ApiError>)
      return false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const register = async (form: RegisterForm) => {
    try {
      await apiClient.post(API_ENDPOINTS.AUTH.SIGN_UP, form)
      return true
    } catch (error) {
      handleApiError(error as AxiosError<ApiError>)
      return false
    }
  }
    
  const fetchCurrentUser = async () => {
    try {
      const response = await apiClient.get(API_ENDPOINTS.AUTH.ME)
      user.value = response.data
    } catch (error) {
      handleApiError(error as AxiosError<ApiError>)
    }
  }
  
  return {
    user,
    isAuthenticated,
    initialized,
    login,
    register,
    logout,
    initialize,
    fetchCurrentUser
  }
})