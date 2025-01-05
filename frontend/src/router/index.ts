// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/register',
        component: () => import('@/views/RegisterView.vue'),
        meta: { requiresGuest: true }  // 追加：ゲストのみアクセス可
      },
      {
        path: '/login',
        component: () => import('@/views/LoginView.vue'),
        meta: { requiresGuest: true }  // 追加：ゲストのみアクセス可
      },
      {
        path: '/',
        component: () => import('@/views/HomeView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/admin/users',
        component: () => import('@/views/admin/UsersView.vue'),
        meta: { 
          requiresAuth: true,
          requiresAdmin: true  // 管理者権限が必要
        }
      }
    ]
  })

// グローバルガードの設定
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    
    // 初期化が済んでいない場合は初期化を実行
    if (!authStore.initialized) {
        await authStore.initialize()
    }

    // ログインが必要なページへのアクセス制御
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        // リダイレクト元を保存
        next({
        path: '/login',
        query: { redirect: to.fullPath }
        })
        return
    }

    // 管理者権限チェックを追加
    if (to.meta.requiresAdmin && !authStore.user?.is_admin) {
        next('/')
        return
    }

    // ゲスト専用ページへのアクセス制御
    if (to.meta.requiresGuest && authStore.isAuthenticated) {
        next('/')  // ログイン済みの場合はホームへ
        return
    }

    // 認証済みであればそのまま進む
    next()
})

export default router