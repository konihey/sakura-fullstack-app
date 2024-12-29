<template>
  <div>
    <h1>Vue + Flask App</h1>
    <el-button @click="testBackend">Test API</el-button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

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