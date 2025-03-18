from flask import Blueprint, request, jsonify
from models.user import User
from models import db
import hashlib
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return jsonify({
            'success': False,
            'message': '邮箱已被注册'
        }), 400

    hashed_password = hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()
    code = data.get('invatationCode')
    level = 1
    if code == '2TX65RS':
        level = 2
    elif code == '8VB2KUN':
        level = 3

    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=hashed_password,
        created_at=datetime.now(),
        level=level
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': '注册成功'
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': '邮箱和密码不能为空'
            }), 400

        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user.password != hashed_password:
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401

        token = create_access_token(identity={'user_id': user.id, 'level': user.level, 'email': user.email}, expires_delta=timedelta(days=1))

        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'level': user.level
                }
            }
        })

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': f'登录失败: '
        }), 500
