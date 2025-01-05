# 認証システムの技術ドキュメント

## 概要
フロントエンド（Vue.js + Pinia）とバックエンド（Flask）を連携したJWTベースの認証システムの実装について解説します。

## アーキテクチャ

### フロントエンド（Vue.js + Pinia）

#### 状態管理（Pinia Store）
```typescript
// stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  // ログイン処理
  const login = async (credentials: LoginForm) => {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials)
    token.value = response.data.access_token
    localStorage.setItem('token', response.data.access_token)
    user.value = response.data.user
  }
})
```

#### API通信（Axios）
インターセプター：通信の前後に割り込んで処理を実施。この場合、tokenをconfigに追加。
```typescript
// utils/axios.ts
const apiClient = axios.create({
  baseURL: API_BASE_URL
})

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})
```

### バックエンド（Flask）

#### ユーザーモデル
id：ユニークなID(主キー)を設定。JWTのidentityに使う。
```python
# models/user.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(512))
```

##### ログイン(token発行)
create_access_token(identity=str(user.id))：token発行時にユニークな主キーを渡す
```python
# routes/auth_routes.py
@auth_bp.route('/login', methods=['POST'])
def login():
    # ログイン認証成功時
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    })
```

#### 認証情報利用
@jwt_required()：デコレータを付ける事で、JWTの認証情報があるリクエストのみ受け付ける  
get_jwt_identity()：token発行時に含めたidentityを返す
```python
# routes/auth_routes.py
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
```

## 認証フロー

1. ログイン処理:
   - ユーザーがログインフォームを送信
   - バックエンドで認証
   - JWTトークン生成（ユーザーIDを含む）
   - フロントエンドでトークンを保存

2. 認証済みAPI通信:
   - Axiosインターセプターが自動的にトークンを付与
   - バックエンドで`@jwt_required()`デコレータがトークンを検証
   - `get_jwt_identity()`でユーザーID取得
   - ユーザー固有のデータを返却

## セキュリティ対策

1. トークン管理:
   - JWTトークンはlocalStorageに保存
   - トークンは有効期限付き
   - 認証切れ時は自動的にログアウト

2. APIセキュリティ:
   - 保護が必要なAPIには`@jwt_required()`デコレータを付与
   - パスワードはハッシュ化して保存
   - トークンの改ざん防止（JWT署名）

## 使用方法

### 新しいAPIエンドポイントの保護
```python
@app.route('/api/protected-data')
@jwt_required()  # このデコレータを追加
def get_protected_data():
    user_id = get_jwt_identity()  # 現在のユーザーID取得
    # ユーザー固有のデータを返す
```

### 公開APIエンドポイント
```python
@app.route('/api/public-data')  # デコレータなし
def get_public_data():
    # 誰でもアクセス可能なデータを返す
```

## 注意点
- JWTトークンの有効期限は適切に設定する
- セキュリティが重要なAPIには必ず`@jwt_required()`を付ける
- パスワード関連の処理は必ずハッシュ化する
- トークンの更新（リフレッシュトークン）の実装を検討する