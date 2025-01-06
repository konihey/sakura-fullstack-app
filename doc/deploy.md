// doc/deploy.md
# Flask + Vue.js アプリケーション VPSデプロイメントガイド

## 1. 初期セットアップ

### プロジェクト構成
```
.
├── docker-compose.yml
├── frontend/
├── backend/
└── nginx/
    └── conf.d/
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - frontend
      - backend

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    expose:
      - "5173"
    environment:
      - VITE_API_URL=http://your_vps_ip  # VPSのIPアドレスを設定
      
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    expose:
      - "5000"
    environment:
      - FLASK_DEBUG=1
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fullstack_db
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=fullstack_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    expose:
      - "5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Nginxの設定 (/nginx/conf.d/default.conf)
```nginx
server {
    listen 80;
    server_name your_vps_ip;  # VPSのIPアドレスを設定

    # フロントエンド
    location / {
        proxy_pass http://frontend:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # バックエンドAPI
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 2. デプロイ手順

### 2.1 アプリケーションフォルダの権限設定
```bash
sudo chown -R ユーザー名:ユーザー名 sakura-fullstack-app
sudo chmod -R 775 sakura-fullstack-app
```

### 2.2 フロントエンドの環境設定
```typescript
// src/constants/api.ts
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost'
```

### 2.3 コンテナの起動
```bash
# 既存のコンテナとイメージをクリーンアップ
docker compose down --volumes

# 再ビルドと起動
docker compose up -d --build
```

### 2.4 データベースのマイグレーション
```bash
# バックエンドコンテナに入る
docker compose exec backend sh

# マイグレーションの実行
flask db upgrade
```

## 3. 動作確認項目
1. フロントエンドの表示確認
2. バックエンドAPIへの接続確認
3. ユーザー登録・ログイン機能の確認
4. データベースの接続確認

## 4. トラブルシューティング

### 4.1 フロントエンドのビルドエラー
```bash
docker compose down --volumes
docker compose up -d --build
```

### 4.2 APIアクセスエラー
- フロントエンドの環境変数（VITE_API_URL）がVPSのIPアドレスに設定されているか確認
- ブラウザの開発者ツールでネットワークタブを確認

### 4.3 データベースエラー
```bash
docker compose exec backend sh
flask db upgrade
```

## 5. GitHubへのコード管理

### 5.1 Personal Access Tokenの設定
1. GitHubの設定ページで生成
   - Settings → Developer settings → Personal access tokens
   - Tokens (classic) → Generate new token (classic)
   - 権限は最低限`repo`を選択

2. VPSでの認証情報設定
```bash
git config --global credential.helper store
git push  # ユーザー名とトークンを入力
```

## 6. 運用上の注意点
1. 環境変数の管理（開発環境と本番環境の区別）
2. データベースのバックアップ
3. ログの定期的な確認
4. セキュリティアップデートの適用

## 7. セキュリティ考慮事項
1. 本番環境ではDEBUGモードを無効化
2. 適切なファイアウォール設定
3. SSL/TLS証明書の設定（必要に応じて）
4. 定期的なセキュリティアップデート