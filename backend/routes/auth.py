from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from models import db, User, UsageRecord
import functools

bp = Blueprint('auth', __name__)

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        membership_type='free',
        daily_edit_limit=10,
        daily_save_limit=5,
        daily_export_limit=3
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'membership_type': new_user.membership_type,
            'daily_edit_limit': new_user.daily_edit_limit,
            'daily_save_limit': new_user.daily_save_limit,
            'daily_export_limit': new_user.daily_export_limit
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar,
            'membership_type': user.membership_type,
            'daily_edit_limit': user.daily_edit_limit,
            'daily_save_limit': user.daily_save_limit,
            'daily_export_limit': user.daily_export_limit
        }
    }), 200

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    today = datetime.utcnow().date()
    
    usage = UsageRecord.query.filter_by(
        user_id=current_user.id,
        usage_date=today
    ).first()
    
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'avatar': current_user.avatar,
            'membership_type': current_user.membership_type,
            'daily_edit_limit': current_user.daily_edit_limit,
            'daily_save_limit': current_user.daily_save_limit,
            'daily_export_limit': current_user.daily_export_limit,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        },
        'usage_today': {
            'edit_count': usage.edit_count if usage else 0,
            'save_count': usage.save_count if usage else 0,
            'export_count': usage.export_count if usage else 0
        }
    }), 200

@bp.route('/check-limit', methods=['POST'])
@token_required
def check_limit(current_user):
    data = request.get_json()
    action_type = data.get('action_type')
    
    if not action_type or action_type not in ['edit', 'save', 'export']:
        return jsonify({'error': 'Invalid action type'}), 400
    
    today = datetime.utcnow().date()
    
    usage = UsageRecord.query.filter_by(
        user_id=current_user.id,
        usage_date=today
    ).first()
    
    if not usage:
        usage = UsageRecord(
            user_id=current_user.id,
            usage_date=today,
            edit_count=0,
            save_count=0,
            export_count=0
        )
        db.session.add(usage)
        db.session.commit()
    
    limit_map = {
        'edit': current_user.daily_edit_limit,
        'save': current_user.daily_save_limit,
        'export': current_user.daily_export_limit
    }
    
    count_map = {
        'edit': usage.edit_count,
        'save': usage.save_count,
        'export': usage.export_count
    }
    
    limit = limit_map[action_type]
    current_count = count_map[action_type]
    
    if current_count >= limit:
        return jsonify({
            'allowed': False,
            'message': f'Daily {action_type} limit reached',
            'limit': limit,
            'used': current_count,
            'remaining': 0
        }), 200
    
    return jsonify({
        'allowed': True,
        'limit': limit,
        'used': current_count,
        'remaining': limit - current_count
    }), 200

@bp.route('/record-usage', methods=['POST'])
@token_required
def record_usage(current_user):
    data = request.get_json()
    action_type = data.get('action_type')
    
    if not action_type or action_type not in ['edit', 'save', 'export']:
        return jsonify({'error': 'Invalid action type'}), 400
    
    today = datetime.utcnow().date()
    
    usage = UsageRecord.query.filter_by(
        user_id=current_user.id,
        usage_date=today
    ).first()
    
    if not usage:
        usage = UsageRecord(
            user_id=current_user.id,
            usage_date=today,
            edit_count=0,
            save_count=0,
            export_count=0
        )
        db.session.add(usage)
    
    if action_type == 'edit':
        usage.edit_count += 1
    elif action_type == 'save':
        usage.save_count += 1
    elif action_type == 'export':
        usage.export_count += 1
    
    db.session.commit()
    
    return jsonify({
        'message': 'Usage recorded',
        'action_type': action_type,
        'count': getattr(usage, f'{action_type}_count')
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200
