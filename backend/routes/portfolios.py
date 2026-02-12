from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import os
from models import db, Portfolio, Category, Tag, Image

bp = Blueprint('portfolios', __name__)

def get_server_url():
    host = current_app.config.get('SERVER_HOST', 'localhost')
    port = current_app.config.get('SERVER_PORT', '5000')
    return f"http://{host}:{port}"

# 获取作品集列表
@bp.route('/', methods=['GET'])
def get_portfolios():
    # 支持按客户名称、拍摄日期筛选
    client_name = request.args.get('client_name')
    shoot_date = request.args.get('shoot_date')
    
    query = Portfolio.query
    
    if client_name:
        query = query.filter(Portfolio.client_name.ilike(f'%{client_name}%'))
    
    if shoot_date:
        try:
            shoot_date_obj = datetime.strptime(shoot_date, '%Y-%m-%d').date()
            query = query.filter(Portfolio.shoot_date == shoot_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid shoot date format'}), 400
    
    portfolios = query.all()
    
    return jsonify({
        'portfolios': [{
            'id': portfolio.id,
            'name': portfolio.name,
            'client_name': portfolio.client_name,
            'shoot_date': portfolio.shoot_date.strftime('%Y-%m-%d'),
            'cover_image': portfolio.cover_image,
            'category_id': portfolio.category_id,
            'image_count': len(portfolio.images),
            'created_at': portfolio.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for portfolio in portfolios]
    }), 200

# 创建作品集
@bp.route('/', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['name', 'client_name', 'shoot_date', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        shoot_date_obj = datetime.strptime(data['shoot_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid shoot date format'}), 400
    
    # 创建作品集
    new_portfolio = Portfolio(
        name=data['name'],
        client_name=data['client_name'],
        shoot_date=shoot_date_obj,
        user_id=data['user_id'],
        category_id=data.get('category_id')
    )
    
    # 处理标签
    if 'tag_ids' in data:
        tags = Tag.query.filter(Tag.id.in_(data['tag_ids'])).all()
        new_portfolio.tags = tags
    
    db.session.add(new_portfolio)
    db.session.commit()
    
    return jsonify({
        'message': 'Portfolio created successfully',
        'portfolio': {
            'id': new_portfolio.id,
            'name': new_portfolio.name,
            'client_name': new_portfolio.client_name,
            'shoot_date': new_portfolio.shoot_date.strftime('%Y-%m-%d')
        }
    }), 201

@bp.route('/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    images = Image.query.filter_by(portfolio_id=portfolio_id).order_by(Image.sort_order).all()
    
    server_url = get_server_url()
    
    return jsonify({
        'portfolio': {
            'id': portfolio.id,
            'name': portfolio.name,
            'client_name': portfolio.client_name,
            'shoot_date': portfolio.shoot_date.strftime('%Y-%m-%d'),
            'cover_image': portfolio.cover_image,
            'category_id': portfolio.category_id,
            'user_id': portfolio.user_id,
            'tags': [tag.id for tag in portfolio.tags],
            'images': [{
                'id': img.id,
                'filename': img.filename,
                'filepath': f'{server_url}/uploads/{os.path.basename(img.filepath)}',
                'thumbnail_path': f'{server_url}/uploads/{os.path.basename(img.thumbnail_path)}',
                'sort_order': img.sort_order
            } for img in images],
            'created_at': portfolio.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': portfolio.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 200

# 更新作品集
@bp.route('/<int:portfolio_id>', methods=['PUT'])
def update_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'name' in data:
        portfolio.name = data['name']
    
    if 'client_name' in data:
        portfolio.client_name = data['client_name']
    
    if 'shoot_date' in data:
        try:
            portfolio.shoot_date = datetime.strptime(data['shoot_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid shoot date format'}), 400
    
    if 'category_id' in data:
        portfolio.category_id = data['category_id']
    
    if 'tag_ids' in data:
        tags = Tag.query.filter(Tag.id.in_(data['tag_ids'])).all()
        portfolio.tags = tags
    
    if 'cover_image' in data:
        portfolio.cover_image = data['cover_image']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Portfolio updated successfully',
        'portfolio': {
            'id': portfolio.id,
            'name': portfolio.name,
            'client_name': portfolio.client_name
        }
    }), 200

# 删除作品集
@bp.route('/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    # 删除关联的图片
    for image in portfolio.images:
        db.session.delete(image)
    
    # 删除作品集
    db.session.delete(portfolio)
    db.session.commit()
    
    return jsonify({'message': 'Portfolio deleted successfully'}), 200

# 获取分类列表
@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    
    return jsonify({
        'categories': [{
            'id': category.id,
            'name': category.name
        } for category in categories]
    }), 200

# 获取标签列表
@bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    
    return jsonify({
        'tags': [{
            'id': tag.id,
            'name': tag.name
        } for tag in tags]
    }), 200