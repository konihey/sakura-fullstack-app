<!-- src/views/admin/UsersView.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import apiClient from '@/utils/axios'
import type { User } from '@/types/user'
import { API_ENDPOINTS } from '@/constants/api'

const users = ref<User[]>([])
const loading = ref(false)

const fetchUsers = async () => {
  try {
    loading.value = true
    const response = await apiClient.get(API_ENDPOINTS.USERS.LIST)
    users.value = response.data
  } catch (error) {
    ElMessage.error('ユーザー一覧の取得に失敗しました')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (userId: number) => {
  try {
    await ElMessageBox.confirm(
      'このユーザーを削除しますか？',
      '確認',
      {
        confirmButtonText: '削除',
        cancelButtonText: 'キャンセル',
        type: 'warning'
      }
    )

    await apiClient.delete(API_ENDPOINTS.USERS.DELETE(userId))
    ElMessage.success('ユーザーを削除しました')
    fetchUsers()  // 一覧を再取得
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('ユーザーの削除に失敗しました')
    }
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">ユーザー管理</h1>
    
    <el-card>
      <el-table 
        :data="users" 
        v-loading="loading"
        style="width: 60%"
      >
        <el-table-column 
          prop="id" 
          label="ID" 
          width="100" 
        />
        <el-table-column 
          prop="username" 
          label="ユーザー名" 
        />
        <el-table-column 
          prop="email" 
          label="メールアドレス" 
        />
        <el-table-column 
          prop="is_admin" 
          label="管理者"
          width="120"
        >
          <template #default="{ row }">
            <el-tag 
              :type="row.is_admin ? 'success' : 'primary'"
              size="small"
            >
              {{ row.is_admin ? '管理者' : '一般' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column 
          label="操作"
          width="120"
          fixed="right"
        >
          <template #default="{ row }">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row.id)"
            >
              削除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>