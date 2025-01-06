# backend/scripts/create_admin.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User

def create_initial_admin(username, email, password):
    """初期管理者アカウントを作成するスクリプト"""
    app = create_app()
    
    with app.app_context():
        try:
            admin = User(
                username=username,
                email=email,
                is_admin=True
            )
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f"管理者アカウントが作成されました: {username}")
            return True
            
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使用方法: python create_admin.py <username> <email> <password>")
        sys.exit(1)
        
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_initial_admin(username, email, password)