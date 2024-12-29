<!-- src/components/UserList.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  created_at: string
  updated_at: string
}

const users = ref<User[]>([])
const loading = ref(true)

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/users/')
    users.value = response.data
  } catch (error) {
    ElMessage.error('ユーザー情報の取得に失敗しました')
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const createTestData = async () => {
  try {
    loading.value = true
    await axios.post('http://localhost:5000/api/users/seed')
    ElMessage.success('テストデータを作成しました')
    await fetchUsers()
  } catch (error: any) {
    if (error.response?.status === 400) {
      ElMessage.warning('すでにユーザーが存在します')
    } else {
      ElMessage.error('テストデータの作成に失敗しました')
    }
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="p-4">
    <div class="mb-4 flex justify-between items-center">
      <h2 class="text-2xl font-bold">ユーザー一覧</h2>
      <el-button type="primary" @click="createTestData" :loading="loading">
        テストデータ作成
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="users"
      style="width: 100%"
      border
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="ユーザー名" width="180" />
      <el-table-column prop="email" label="メールアドレス" width="220" />
      <el-table-column prop="created_at" label="作成日時">
        <template #default="scope">
          {{ new Date(scope.row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>