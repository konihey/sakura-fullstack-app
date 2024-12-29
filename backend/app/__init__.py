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
    
    # ルートの登録
    from app.routes.api import api_bp
    from app.routes.user_routes import user_bp
    from app.routes.task_routes import task_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    
    return app