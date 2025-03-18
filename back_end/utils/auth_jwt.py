from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['user_id']).first()
        if not user:
            return jsonify({'message': '用户不存在'}), 401
        return f(user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if current_user['level'] < 3:  # Check if user is admin
            return jsonify({'message': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated
