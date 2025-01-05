// src/components/LoginForm.vue
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()  // 追加
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('ユーザー名とパスワードを入力してください')
    return
  }
  
  loading.value = true
  try {
    const success = await authStore.login({
      username: form.value.username,
      password: form.value.password
    })
    
    if (success) {
      ElMessage.success('ログインしました')
      // リダイレクト先が指定されている場合はそこへ、なければホームへ
      const redirectPath = (route.query.redirect as string) || '/'
      router.push(redirectPath)
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <el-form-item label="ユーザー名">
      <el-input 
        v-model="form.username"
        placeholder="ユーザー名を入力"
        autocomplete="username"
      />
    </el-form-item>
    
    <el-form-item label="パスワード">
      <el-input 
        v-model="form.password"
        type="password"
        placeholder="パスワードを入力"
        autocomplete="current-password"
      />
    </el-form-item>
    
    <div>
      <el-button 
        type="primary"
        native-type="submit"
        :loading="loading"
        class="w-full"
      >
        ログイン
      </el-button>
    </div>
    
    <div class="text-center text-sm">
      <router-link 
        to="/register"
        class="text-blue-600 hover:text-blue-700"
      >
        新規登録はこちら
      </router-link>
    </div>
  </form>
</template>