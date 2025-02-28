// README.md
これはさくらVPSにvueフルスタックアプリのアップするための練習です。

**フロントエンド（Vue.js）:**
- Vue 3 + Composition API
- Element Plus（UIコンポーネント）
- Vue Router（ルーティング）
- Pinia（状態管理、Vuexの後継）
- Axios（APIクライアント）

**バックエンド（Flask）:**
- Flask RESTful（APIエンドポイント）
- Flask-SQLAlchemy（ORマッパー）
- Flask-Migrate（DBマイグレーション）
- Flask-JWT-Extended（認証）
- Flask-CORS（CORS対応）

**データベース:**
- PostgreSQL

**インフラ:**
- Docker / Docker Compose
  - フロントエンドコンテナ
  - バックエンドコンテナ
  - DBコンテナ
- Nginx（リバースプロキシ）
- さくらVPS

**開発環境:**
- Git（ソース管理）
- VSCode
- DBeaver（DBクライアント）など

基本的なディレクトリ構成：
```bash
fullstack-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/
│   │   └── api/
│   └── Dockerfile
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   └── Dockerfile
├── nginx/
│   └── conf.d/
└── docker-compose.yml
```

# さくらVPS フルスタックアプリ開発 - 状況報告

## 現在の実装状況

### 環境構築
- Docker Composeによる3コンテナ構成（frontend, backend, db）
- 各コンテナ間の通信確認済み
- 基本的なCORS設定完了

### フロントエンド（Vue.js + Element Plus）
- 開発環境としてViteを使用
- 基本的なコンポーネント構造の実装
- バックエンドAPIとの疎通確認済み
- ホットリロード等の開発環境が正常に動作

### バックエンド（Flask）
- 基本的なAPIエンドポイント（/api/test）の実装
- CORSの設定完了
- フロントエンドからのリクエストに正常に応答

### データベース（PostgreSQL）
- コンテナ起動確認済み
- 基本的な設定完了
- まだアプリケーションからの接続は未実装

## 技術スタックの理解
- Viteの役割（開発サーバー、ビルドツール）
- Vue.jsとViteの関係
- 開発環境とデプロイ環境の違い
- Nginxの役割（Webサーバー、リバースプロキシ）

## 次のステップ
1. データベース実装
   - テーブル設計
   - サンプルデータの作成
   - マイグレーション設定

2. バックエンドAPI拡張
   - DBアクセス用のモデル作成
   - CRUD操作用のエンドポイント実装
   - エラーハンドリング

3. フロントエンド機能追加
   - APIクライアントの実装
   - データ表示用のコンポーネント作成
   - データ操作用のフォーム実装

## 保留中の課題
- 本番環境用のDocker設定
- SSL/TLS設定
- 認証機能の実装


# Flask SQLAlchemy + Blueprint ベストプラクティス

## 1. プロジェクト構成
```
backend/
├── app/
│   ├── __init__.py        # アプリケーション初期化、DB設定
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py        # Userモデル
│   │   └── task.py        # Taskモデル
│   └── routes/
│       ├── __init__.py
│       ├── user_routes.py  # ユーザー関連API
│       └── task_routes.py  # タスク関連API
├── app.py                 # アプリケーションエントリーポイント
├── Dockerfile
└── requirements.txt
```

## 2. コアファイルの設定

### アプリケーション初期化と設定
```python
# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/fullstack_db'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # モデルを明示的にインポート
    from app.models.user import User
    from app.models.task import Task
    
    # Blueprintの登録
    from app.routes.user_routes import user_bp
    from app.routes.task_routes import task_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    
    return app
```

### モデル定義
```python
# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### API Blueprint実装
```python
# app/routes/user_routes.py
from flask import Blueprint, jsonify, request
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
```

## 3. データベースマイグレーション手順

### 初回セットアップ
```bash
# 環境のクリーンアップ
docker compose down -v
rm -rf backend/migrations

# コンテナ起動
docker compose up --build

# 別ターミナルでマイグレーション実行
docker compose exec backend flask db init
docker compose exec backend flask db migrate -m "Initial migration"
docker compose exec backend flask db upgrade
```

### モデル変更時のマイグレーション
```bash
# モデル変更後、マイグレーションファイル作成
docker compose exec backend flask db migrate -m "変更の説明"

# 変更をDBに適用
docker compose exec backend flask db upgrade
```

### マイグレーションの確認
```bash
# DBの状態確認
docker compose exec db psql -U postgres fullstack_db -c "\dt"
docker compose exec db psql -U postgres fullstack_db -c "\d users"
```

## 4. プラクティスの重要ポイント

### 1. アプリケーション全体の設計
- アプリケーション初期化とDB設定を`__init__.py`で一元管理
- `create_app()`内でモデルを明示的にインポート（Flask-Migrateのモデル認識に必須）
- 関心事の分離による保守性の向上
- モジュール性の確保

### 2. Blueprint によるAPI設計
- 機能ごとにルートを分割
- URLプレフィックスによる体系的な整理（例：`/api/users/`, `/api/tasks/`）
- エンドポイントの保守が容易
- チーム開発での分業がしやすい
- 機能追加・拡張が容易

### 3. データベース管理とマイグレーション
- マイグレーションは手動で明示的に実行
- モデル変更はマイグレーションファイルを通して管理
- 変更履歴を明確に記録
- 意図しない変更を防止
- 開発環境でのデータ永続化はDockerボリュームで実現

### 4. ファイル構成と実装方針
- モデルは`app/models/`内で個別に定義
- APIルートは`app/routes/`でBlueprintとして実装
- 環境固有の設定は環境変数で管理
- 明確なディレクトリ構造による可読性の向上
- モジュール単位でのテストが容易

このアーキテクチャにより：
1. コードの保守性と拡張性が向上
2. チーム開発での効率が上がる
3. 変更履歴の追跡が容易になる
4. 機能追加が体系的に行える
5. テストと品質管理が効率化される


# さくらVPS フルスタックアプリ開発 - 進捗更新

## 実装完了項目（2024年12月29日）

### データベース実装
- PostgreSQLコンテナの初期設定完了
- マイグレーション機能の実装と動作確認
  - Flask-Migrateによるマイグレーション設定
  - Userモデルの初期マイグレーション成功
  - テストデータのシーディング機能実装

### バックエンド拡張
- User モデルの実装
  - 基本的なCRUD操作の準備
  - to_dict メソッドによるJSON変換対応
- Blueprint によるルーティング実装
  - GET /api/users/ エンドポイントの実装
  - GET /api/users/<id> エンドポイントの実装
  - POST /api/users/seed テストデータ作成エンドポイントの実装

### フロントエンド実装
- コンポーネント構造の整備
  - src/components ディレクトリの構造化
  - UserList コンポーネントの実装
- Element Plus による UI 実装
  - ユーザー一覧表示機能
  - テストデータ作成ボタンの実装
- APIとの連携
  - Axiosによるバックエンドとの通信確認
  - エラーハンドリングの実装
  - ローディング状態の実装

# JWT認証機能の実装状況（2024/01/04更新）

## 実装完了した機能

### バックエンド（Flask）
- ユーザーモデルの実装（パスワードハッシュ化対応）
- 認証関連エンドポイントの実装
  - POST /api/auth/register - ユーザー登録
  - POST /api/auth/login - ログイン
  - GET /api/auth/me - 現在のユーザー情報取得
- エラーハンドリングの改善
  - バリデーションエラーの詳細表示
  - エラーレスポンスの形式統一
  - DBエラーのハンドリング

### フロントエンド（Vue.js）
- Pinia による認証状態管理（useAuthStore）
- Vue Router によるルーティング設定
  - /register - 新規登録画面
  - /login - ログイン画面
  - / - ホーム画面（要認証）
- 型定義の整備
  - User インターフェース
  - LoginForm/RegisterForm インターフェース
  - ApiError インターフェース
- コンポーネントの実装
  - App.vue - メインレイアウト
  - HomeView.vue - ホーム画面
  - RegisterView.vue - 登録画面
  - LoginView.vue - ログイン画面
  - UserList.vue - ユーザー一覧

### 環境設定
- Viteの設定調整
  - HMRの有効化
  - ファイル監視の設定
  - @エイリアスの設定
- APIクライアントの共通設定
- エラーハンドリングの共通処理

## 次のステップ
1. ユーザー登録機能のテスト
2. ログイン/ログアウト機能のテスト
3. 認証状態の永続化確認
4. エラーメッセージの表示確認
5. バリデーションの動作確認

## 開発環境の起動方法
```bash
# コンテナのビルドと起動
docker compose up -d --build

# バックエンドのマイグレーション実行
docker compose exec backend flask db upgrade

# 各サービスへのアクセス
フロントエンド: http://localhost:5173
バックエンドAPI: http://localhost:5000
```

## 技術スタック
- フロントエンド
  - Vue 3 + TypeScript
  - Vue Router
  - Pinia（状態管理）
  - Element Plus（UIコンポーネント）
- バックエンド
  - Flask
  - Flask-JWT-Extended
  - SQLAlchemy
- インフラ
  - Docker/Docker Compose
  - PostgreSQL

## 注意事項
- 開発環境での実装のため、本番環境用の設定は未実装
- セキュリティ設定は最小限の実装
- 環境変数による設定は未実装
- データベースのマイグレートは不要だった（テーブル構成は変えていない）

# Vue + Flask JWT認証実装の技術検討履歴（2025/01/05）

## 1. 「ユーザー情報を取得」ボタンのエラー解決
### 問題
- ユーザー情報取得ボタンを押すと、問答無用でエラーが発生
- コンポーネントからストアの関数にアクセスできない状態

### 解決策
- Piniaストアのreturn文に`fetchCurrentUser`を追加
```typescript
return {
  user,
  isAuthenticated,
  login,
  register,
  logout,
  initialize,
  fetchCurrentUser  // 追加
}
```

### 学んだこと
- Piniaストアでは、外部から利用したい関数を明示的にreturnする必要がある
- ストア内で定義した関数は、デフォルトではプライベート
- コンポーネントからアクセスするには、returnで公開する必要がある

## 2. ホーム画面リロード時の認証状態解除
### 問題
- ページをリロードすると強制的にログイン画面に遷移
- LocalStorageにトークンが残っているのに認証状態が維持されない

### 解決策
1. ルーターガードの実装
2. 認証状態の初期化処理の追加
3. トークンの永続化（LocalStorage）の確認

### ルーター設定 (router/index.ts)
```typescript
// グローバルガードの設定
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 初期化が済んでいない場合は初期化を実行
  if (!authStore.initialized) {
    await authStore.initialize()
  }

  // ログインが必要なページへのアクセスをチェック
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

### Piniaストアの設定 (stores/auth.ts)
```typescript
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const initialized = ref(false) // この部分！！

  const isAuthenticated = computed(() => !!token.value)

  // 初期化処理
  const initialize = async () => {
    try {
      const savedToken = localStorage.getItem('token')
      if (savedToken) {
        token.value = savedToken
        await fetchCurrentUser()
      }
    } catch (error) {
      console.error('Initialization failed:', error)
      logout()
    } finally {
      initialized.value = true // この部分！！
    }
  }

  return {
    user,
    token,
    initialized, // この部分！！
    isAuthenticated,
    initialize,
    // ... 他のメソッド
  }
})
```

### 重要なポイント
- SPAではページリロード時にステート（状態）が初期化される
- LocalStorageのトークンを使って再認証する必要がある
- ルーティング判断前に認証状態を復元することが重要

## 3. バックエンドのログ出力
### 問題
- 認証エラーの原因特定が困難
- トークンの受け渡しが正しく行われているか確認できない

## 2. ログ出力の設定
### Flask側の設定

1. エンドポイントでのログ出力 (routes/auth_routes.py)
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # これが重要！この部分があるとdocker-compose logsでDEBUG表示できる

# ... 他のコード

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    logger = logging.getLogger(__name__)
    logger.debug("=== /me エンドポイントが呼び出されました ===")
    logger.debug(f"Request Headers: {dict(request.headers)}")
    # ... 他のログ出力
```

### 効果的だった点
- リクエストヘッダーの詳細な確認が可能に
- トークンの受け渡し状況の可視化
- エラーの発生箇所の特定が容易に

## 教訓
1. **状態管理の重要性**
   - SPAでの状態管理は慎重に設計する必要がある
   - 特に認証情報の永続化と復元は重要

2. **デバッグの重要性**
   - フロントエンド、バックエンド両方でのログ出力が重要
   - エラーの早期発見と原因特定に必要不可欠

3. **段階的な実装の有効性**
   - 基本機能から段階的に実装することで問題を分離できる
   - エラーが発生した際の原因特定が容易になる

申し訳ありません。確かにその通りです。私の整理が間違っていました。
これらは既に実装完了した機能として報告すべきですね。

# 認証機能実装進捗報告書 (2025/01/05)

## 1. 実装完了機能

### ユーザー認証基盤
- ユーザー登録フロー
  - バリデーション実装
  - エラーメッセージ表示
  - 登録成功時の遷移処理

- ログイン/ログアウトフロー
  - LocalStorageによる認証状態の永続化
  - トークン有効期限の設定と確認
  - ログアウト時の状態クリア処理

### JWT実装
- トークンの有効期限設定
- 401エラー時の自動ログアウト
- トークン管理の整備

### アクセス制御
- 未認証ユーザーの自動リダイレクト
- 認証済みユーザーのアクセス制御
- ルートティング時の適切な権限反映

### 管理者機能
- コマンドラインからの管理者ユーザー作成
- ユーザー一覧表示と削除機能
- 管理者自身の削除防止機能

### コード整備
- API実装のリファクタリング完了

## 2. 技術的知見
- SPAの基幹システム構成の重要性を確認
  - Vue Router（`/src/router/index.ts`）：ルーティング制御
  - Pinia Store（`/src/stores/auth.ts`）：状態管理

### **実施済み**
- レポジトリのgithubへのアップ
  - 公開設定でclone
  - tokenを発行してパスワードとしてpush
- 環境変数による設定の一部
  - API_URL（VITE_API_URL）
  - データベース接続情報（DATABASE_URL）
- NGINXの設定の一部
  - 基本的なリバースプロキシ設定

### **未実施**
- 環境変数による設定
  - JWT設定（秘密鍵）
  - その他の環境依存値
- NGINXの設定
  - SSL/TLS設定
  - キャッシュ設定
  - セキュリティヘッダー
- 本番用Docker設定
  - マルチステージビルド
  - 最適化設定
  - ヘルスチェック
  - ログローテーション

特に優先度が高そうな項目：
1. SSL/TLS設定（Let's Encrypt等の導入）
2. JWT秘密鍵の環境変数化
3. セキュリティヘッダーの追加
4. 本番向けのDockerfile最適化
