# Vue + Flask フルスタックアプリのSSL/TLS設定手順

## 1. 前提環境
- DuckDNSドメイン: konitest.duckdns.org
- Ubuntu サーバー（さくらVPS）
- Docker + Docker Compose による構成
- Vue.js + Flask のフルスタックアプリケーション

## 2. 実装手順

### 2.1 nginxの準備
1. ホストマシンのnginxを停止
```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
```

2. 実行中のプロセスを確認・停止
```bash
sudo lsof -i :80
sudo kill -9 [プロセスID]
```

### 2.2 SSL証明書の取得
1. certbotのインストール
```bash
sudo apt update
sudo apt install certbot
```

2. 証明書の取得
```bash
sudo certbot certonly --standalone -d konitest.duckdns.org
```

### 2.3 Nginx設定

`nginx/conf.d/default.conf`:
```nginx
# 共通のSSL設定
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# セキュリティヘッダー
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";

# HTTP -> HTTPS リダイレクト
server {
    listen 80;
    server_name konitest.duckdns.org;
    return 301 https://$server_name$request_uri;
}

# HTTPS設定
server {
    listen 443 ssl;
    server_name konitest.duckdns.org;

    ssl_certificate /etc/letsencrypt/live/konitest.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/konitest.duckdns.org/privkey.pem;

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

### 2.4 Docker Compose設定

`docker-compose.yml`:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /var/lib/letsencrypt:/var/lib/letsencrypt:ro
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
      - VITE_API_URL=https://konitest.duckdns.org
      
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

## 3. アプリケーションの起動
```bash
docker compose up -d --build
```

## 4. 確認事項
- HTTPSアクセス（https://konitest.duckdns.org）が可能
- HTTPからHTTPSへの自動リダイレクト
- 証明書の警告は初回アクセス時のみ表示（DuckDNSドメインの特性）
- フロントエンド・バックエンド間の通信が正常に機能

## 5. セキュリティ設定の効果
- TLS 1.2/1.3の使用による安全な暗号化
- HSTSによるHTTPS強制
- クリックジャッキング対策（X-Frame-Options）
- XSS対策（X-XSS-Protection）
- MIME Type Sniffing対策（X-Content-Type-Options）

## 6. 注意点
- Let's Encrypt証明書は90日で期限切れ（自動更新設定済み）
- DuckDNSドメインの特性上、ブラウザ警告が表示される場合あり
- 本番環境では独自ドメインの使用を推奨