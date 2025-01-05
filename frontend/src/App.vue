<!-- App.vue -->
<!-- アプリケーションの基本構造のみを提供 -->
<template>
    <div class="container mx-auto py-8">
      <!-- ヘッダー部分 -->
      <header class="mb-8">
        <nav class="flex justify-between items-center">
          <h1 class="text-2xl font-bold">Vue + Flask App</h1>
          <HeaderNav />
        </nav>
      </header>
  
      <!-- メインコンテンツ -->
      <main>
        <router-view />
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import HeaderNav from '@/components/HeaderNav.vue'
  
  const authStore = useAuthStore()
  
  // アプリケーションの初期化のみを担当
  onMounted(async () => {
    await authStore.initialize()
  })
  </script>