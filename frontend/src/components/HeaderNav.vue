<!-- components/HeaderNav.vue -->
<!-- ナビゲーション専用コンポーネント -->
<template>
    <div class="space-x-4">
      <template v-if="authStore.isAuthenticated">
        <el-button @click="handleLogout">ログアウト</el-button>
      </template>
      <template v-else>
        <el-button @click="router.push('/login')">ログイン</el-button>
        <el-button type="primary" @click="router.push('/register')">新規登録</el-button>
      </template>
    </div>
  </template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  
  const router = useRouter()
  const authStore = useAuthStore()
  
  const handleLogout = () => {
    authStore.logout()
    router.push('/login')
  }
  </script>