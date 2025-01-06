<!-- components/UserProfile.vue -->
<!-- ユーザープロファイル表示と操作を担当 -->
<template>
    <div class="mb-6 p-4 bg-white shadow rounded">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">現在のユーザー情報</h3>
        <el-button 
          type="primary" 
          @click="fetchUserInfo" 
          :loading="loading"
        >
          ユーザー情報を取得
        </el-button>
      </div>
      
      <div v-if="authStore.user" class="space-y-2">
        <p><strong>ユーザー名:</strong> {{ authStore.user.username }}</p>
        <p><strong>メール:</strong> {{ authStore.user.email }}</p>
        <p><strong>作成日:</strong> {{ authStore.user.created_at }}</p>
      </div>
      <p v-else class="text-gray-500">
        ユーザー情報を取得するにはボタンをクリックしてください
      </p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { ElMessage } from 'element-plus'
  
  const authStore = useAuthStore()
  const loading = ref(false)
  
  const fetchUserInfo = async () => {
    loading.value = true
    try {
      await authStore.fetchCurrentUser()
      ElMessage.success('ユーザー情報を取得しました')
    } catch (error: any) {
      ElMessage.error('ユーザー情報の取得に失敗しました')
    } finally {
      loading.value = false
    }
  }
  </script>