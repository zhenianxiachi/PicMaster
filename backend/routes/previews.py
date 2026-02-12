from flask import Blueprint, request, jsonify, send_from_directory, render_template, current_app
import qrcode
import os
import uuid
from datetime import datetime, timedelta
from models import db, PreviewLink, Portfolio
import io
import base64

bp = Blueprint('previews', __name__)

def get_server_url():
    host = current_app.config.get('SERVER_HOST', 'localhost')
    port = current_app.config.get('SERVER_PORT', '5000')
    return f"http://{host}:{port}"

def get_frontend_url():
    return current_app.config.get('FRONTEND_URL', 'http://localhost:3000')

# 生成预览链接和二维码
@bp.route('/generate', methods=['POST'])
def generate_preview():
    data = request.get_json()
    portfolio_id = data.get('portfolio_id')
    preview_url = data.get('preview_url')
    
    if not portfolio_id:
        return jsonify({'error': 'Portfolio ID is required'}), 400
    
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    token = str(uuid.uuid4())
    expire_time = datetime.utcnow() + timedelta(hours=24)
    
    preview_link = PreviewLink(
        portfolio_id=portfolio_id,
        token=token,
        expire_time=expire_time
    )
    
    db.session.add(preview_link)
    db.session.commit()
    
    if not preview_url:
        frontend_url = get_frontend_url()
        preview_url = f"{frontend_url}/viewer?portfolio_id={portfolio_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(preview_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return jsonify({
        'message': 'Preview link generated successfully',
        'preview_url': preview_url,
        'qr_code': f"data:image/png;base64,{qr_base64}",
        'expire_time': expire_time.strftime('%Y-%m-%d %H:%M:%S'),
        'token': token
    }), 200

# 验证预览链接
@bp.route('/validate/<string:token>', methods=['GET'])
def validate_preview(token):
    preview_link = PreviewLink.query.filter_by(token=token, is_valid=True).first()
    
    if not preview_link:
        return jsonify({'error': 'Invalid or expired preview link'}), 404
    
    # 检查是否过期
    if datetime.utcnow() > preview_link.expire_time:
        # 标记为无效
        preview_link.is_valid = False
        db.session.commit()
        return jsonify({'error': 'Preview link has expired'}), 410
    
    # 获取作品集信息
    portfolio = Portfolio.query.get(preview_link.portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    return jsonify({
        'valid': True,
        'portfolio': {
            'id': portfolio.id,
            'name': portfolio.name,
            'client_name': portfolio.client_name
        },
        'expire_time': preview_link.expire_time.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

# 客户预览页面
@bp.route('/<string:token>', methods=['GET'])
def client_preview(token):
    # 这个路由用于前端渲染预览页面
    # 实际项目中，这里可以返回渲染的HTML页面或JSON数据供前端使用
    return jsonify({
        'token': token,
        'message': 'This is the client preview endpoint'
    }), 200

# 获取预览的作品集数据
@bp.route('/data/<string:token>', methods=['GET'])
def get_preview_data(token):
    preview_link = PreviewLink.query.filter_by(token=token, is_valid=True).first()
    
    if not preview_link:
        return jsonify({'error': 'Invalid or expired preview link'}), 404
    
    # 检查是否过期
    if datetime.utcnow() > preview_link.expire_time:
        preview_link.is_valid = False
        db.session.commit()
        return jsonify({'error': 'Preview link has expired'}), 410
    
    # 获取作品集详情
    portfolio = Portfolio.query.get(preview_link.portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    # 获取作品集中的图片
    images = []
    for image in portfolio.images:
        images.append({
            'id': image.id,
            'filename': image.filename,
            'filepath': image.filepath,
            'thumbnail_path': image.thumbnail_path,
            'sort_order': image.sort_order
        })
    
    return jsonify({
        'portfolio': {
            'id': portfolio.id,
            'name': portfolio.name,
            'client_name': portfolio.client_name,
            'shoot_date': portfolio.shoot_date.strftime('%Y-%m-%d'),
            'images': images
        },
        'expire_time': preview_link.expire_time.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

# 保存客户反馈
@bp.route('/feedback', methods=['POST'])
def save_feedback():
    from models import ClientFeedback
    
    data = request.get_json()
    required_fields = ['portfolio_id', 'client_name', 'feedback_content']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    feedback = ClientFeedback(
        portfolio_id=data['portfolio_id'],
        client_name=data['client_name'],
        feedback_content=data['feedback_content']
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({
        'message': 'Feedback saved successfully',
        'feedback': {
            'id': feedback.id,
            'client_name': feedback.client_name,
            'feedback_content': feedback.feedback_content,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 201