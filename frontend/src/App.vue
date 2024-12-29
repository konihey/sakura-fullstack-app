<!-- src/App.vue -->
<template>
    <div class="container mx-auto py-8">
      <div class="mb-8 space-y-4">
        <h1 class="text-2xl font-bold">Vue + Flask App</h1>
        <div class="flex items-center space-x-4">
          <el-button @click="testBackend">Test API Connection</el-button>
          <p v-if="message" class="text-gray-600">{{ message }}</p>
        </div>
      </div>
      
      <UserList />
    </div>
  </template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import UserList from './components/UserList.vue'

const message = ref('')

const testBackend = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/test')
    message.value = response.data.message
  } catch (error) {
    message.value = 'Error connecting to backend'
  }
}
</script>