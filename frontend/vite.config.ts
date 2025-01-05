import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    watch: {
      usePolling: true  // ファイル変更の監視にポーリングを使用
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')  // @エイリアスの設定
    }
  }
})