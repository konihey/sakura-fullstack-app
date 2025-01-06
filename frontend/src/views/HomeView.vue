<!-- src/views/HomeView.vue -->
<script setup lang="ts">
import UserProfile from '@/components/UserProfile.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
console.log('現在のユーザー:', authStore.user)  // is_adminの値を確認
</script>

<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">ホーム</h1>
    
    <!-- ユーザープロファイル -->
    <UserProfile />
    
    <!-- 管理者の場合のみユーザー管理へのリンクを表示 -->
    <div v-if="authStore.user?.is_admin" class="mt-4">
      <router-link 
        to="/admin/users" 
        class="text-blue-600 hover:text-blue-700"
      >
        ユーザー管理へ
      </router-link>
    </div>
  </div>
</template>