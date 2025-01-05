# app/routes/user_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

def require_admin(f):
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or not current_user.is_admin:
            return jsonify({'message': '管理者権限が必要です'}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@user_bp.route('/', methods=['GET'])
@require_admin
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # 管理者は削除できない
        if user.is_admin:
            return jsonify({'message': '管理者アカウントは削除できません'}), 403
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'ユーザーを削除しました'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'ユーザーの削除に失敗しました'}), 500