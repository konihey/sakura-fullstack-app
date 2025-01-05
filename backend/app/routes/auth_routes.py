# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def validate_registration(data):
   errors = {}
   
   # 必須フィールドのチェック
   required_fields = ['username', 'email', 'password']
   for field in required_fields:
       if not data.get(field):
           errors[field] = [f'{field}は必須です']

   # ユーザー名の重複チェック
   if User.query.filter_by(username=data.get('username')).first():
       errors['username'] = ['このユーザー名は既に使用されています']
       
   # メールアドレスの重複チェック
   if User.query.filter_by(email=data.get('email')).first():
       errors['email'] = ['このメールアドレスは既に登録されています']
       
   # パスワードの長さチェック
   if data.get('password') and len(data['password']) < 8:
       errors['password'] = ['パスワードは8文字以上必要です']
   
   return errors

@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        
        # バリデーション
        errors = validate_registration(data)
        if errors:
            return jsonify({
                'message': '入力内容に誤りがあります',
                'details': errors
            }), 400

        user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'ユーザー登録が完了しました',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({
            'message': 'ユーザー名とパスワードは必須です'
        }), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'ログインしました',
            'access_token': access_token,
            'user': user.to_dict()
        })
    
    return jsonify({
        'message': 'ユーザー名またはパスワードが正しくありません'
    }), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'ユーザーが見つかりません'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'message': str(e)}), 500