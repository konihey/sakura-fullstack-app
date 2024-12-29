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

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username=data['username'],
        email=data['email']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/seed', methods=['POST'])
def seed_users():
    # 既存のユーザーを確認
    if User.query.count() > 0:
        return jsonify({'message': 'Users already exist'}), 400

    test_users = [
        User(username='test_user1', email='user1@example.com'),
        User(username='test_user2', email='user2@example.com'),
        User(username='test_user3', email='user3@example.com'),
        User(username='test_user4', email='user4@example.com'),
        User(username='test_user5', email='user5@example.com')
    ]
    
    try:
        for user in test_users:
            db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Test users created successfully', 'count': len(test_users)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500