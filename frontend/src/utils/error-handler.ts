import { ElMessage } from 'element-plus'
import type { AxiosError } from 'axios'
import type { ApiError } from '@/types/error'

export const handleApiError = (error: AxiosError<ApiError>) => {
  // ネットワークエラー
  if (!error.response) {
    ElMessage.error('サーバーに接続できません。インターネット接続を確認してください。')
    return
  }

  const status = error.response.status
  const errorData = error.response.data

  switch (status) {
    case 400: // バリデーションエラー
      if (errorData.details) {
        // フォームのバリデーションエラーを詳細に表示
        const messages = Object.entries(errorData.details)
          .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
        ElMessage.warning(messages.join('\n'))
      } else {
        ElMessage.warning(errorData.message || '入力内容を確認してください')
      }
      break

    case 401: // 認証エラー
      if (errorData.code === 'token_expired') {
        ElMessage.error('セッションが切れました。再度ログインしてください')
      } else {
        ElMessage.error('ユーザー名またはパスワードが正しくありません')
      }
      break

    case 403: // 権限エラー
      ElMessage.error('この操作を行う権限がありません')
      break

    case 404: // Not Found
      ElMessage.error('リソースが見つかりません')
      break

    case 409: // 競合
      ElMessage.warning('既に登録されているデータです')
      break

    case 422: // バリデーションエラー（別形式）
      ElMessage.warning(errorData.message || 'データの形式が正しくありません')
      break

    case 429: // レートリミット
      ElMessage.warning('リクエストが多すぎます。しばらく待ってから再試行してください')
      break

    case 500: // サーバーエラー
      ElMessage.error('サーバーエラーが発生しました。しばらく時間をおいて再度お試しください')
      break

    default:
      ElMessage.error('予期せぬエラーが発生しました')
  }

  // 開発時のみコンソールにエラー詳細を出力
  if (import.meta.env.DEV) {
    console.error('API Error:', {
      status,
      data: errorData,
      url: error.config?.url,
      method: error.config?.method
    })
  }
}