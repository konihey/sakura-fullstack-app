from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False  # URLの末尾スラッシュを柔軟に扱う

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],  # Viteのデフォルトポート
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/fullstack_db'
    # JWT設定の拡充
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 本番環境では環境変数から読み込む
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    # app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) # リフレッシュトークンは今回は不要
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # 追加
    
    from app.models.user import User
    from app.models.task import Task
    
    from app.routes.sample_routes import sample_bp
    from app.routes.user_routes import user_bp
    from app.routes.task_routes import task_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(sample_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)
    
    return app