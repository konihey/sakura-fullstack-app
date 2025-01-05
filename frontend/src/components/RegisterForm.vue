// src/components/RegisterForm.vue
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
  is_admin: false
})

const loading = ref(false)

const validateForm = () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    ElMessage.warning('全ての項目を入力してください')
    return false
  }
  
  if (form.value.password !== form.value.passwordConfirm) {
    ElMessage.warning('パスワードが一致しません')
    return false
  }
  
  return true
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  loading.value = true
  try {
    const success = await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      is_admin: form.value.is_admin
    })
    
    if (success) {
      ElMessage.success('登録が完了しました')
      router.push('/login')
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
    
    <el-form-item label="メールアドレス">
      <el-input 
        v-model="form.email"
        type="email"
        placeholder="メールアドレスを入力"
        autocomplete="email"
      />
    </el-form-item>
    
    <el-form-item label="パスワード">
      <el-input 
        v-model="form.password"
        type="password"
        placeholder="パスワードを入力"
        autocomplete="new-password"
      />
    </el-form-item>
    
    <el-form-item label="パスワード（確認）">
      <el-input 
        v-model="form.passwordConfirm"
        type="password"
        placeholder="パスワードを再入力"
        autocomplete="new-password"
      />
    </el-form-item>
    
    <el-form-item>
      <el-checkbox v-model="form.is_admin">管理者として登録</el-checkbox>
    </el-form-item>

    <div>
      <el-button 
        type="primary"
        native-type="submit"
        :loading="loading"
        class="w-full"
      >
        登録する
      </el-button>
    </div>
    
    <div class="text-center text-sm">
      <router-link 
        to="/login"
        class="text-blue-600 hover:text-blue-700"
      >
        既にアカウントをお持ちの方はこちら
      </router-link>
    </div>
  </form>
</template>