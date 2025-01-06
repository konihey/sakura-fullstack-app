<!-- // src/views/LoginView.vue -->
<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue'
import { ElResult } from 'element-plus'
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="text-center text-3xl font-bold tracking-tight text-gray-900">
        ログイン
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <LoginForm />
      </div>
    </div>
  </div>
</template>
