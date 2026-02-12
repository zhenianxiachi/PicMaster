from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageFilter, ImageEnhance
import json
import uuid
from models import db, Image, Portfolio

bp = Blueprint('images', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_server_url():
    host = current_app.config.get('SERVER_HOST', 'localhost')
    port = current_app.config.get('SERVER_PORT', '5000')
    return f"http://{host}:{port}"

# 图片上传
@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('file')
    portfolio_id = request.form.get('portfolio_id')
    
    if not portfolio_id:
        return jsonify({'error': 'Portfolio ID is required'}), 400
    
    # 检查作品集是否存在
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # 确保上传目录存在
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # 保存文件到上传目录
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)
            
            # 生成缩略图
            thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"thumb_{unique_filename}")
            try:
                generate_thumbnail(upload_path, thumbnail_path)
            except Exception as e:
                print(f"生成缩略图失败: {str(e)}")
                # 如果缩略图生成失败，使用原图路径
                thumbnail_path = upload_path
            
            # 获取当前最大排序序号
            max_sort = db.session.query(db.func.max(Image.sort_order)).filter_by(portfolio_id=portfolio_id).scalar() or 0
            
            # 保存到数据库
            new_image = Image(
                filename=filename,
                filepath=upload_path,
                thumbnail_path=thumbnail_path,
                sort_order=max_sort + 1,
                portfolio_id=portfolio_id
            )
            db.session.add(new_image)
            uploaded_files.append(new_image)
    
    db.session.commit()
    
    server_url = get_server_url()
    
    return jsonify({
        'message': 'Images uploaded successfully',
        'images': [{
            'id': img.id,
            'filename': img.filename,
            'filepath': f'{server_url}/uploads/{os.path.basename(img.filepath)}',
            'thumbnail_path': f'{server_url}/uploads/{os.path.basename(img.thumbnail_path)}',
            'sort_order': img.sort_order
        } for img in uploaded_files]
    }), 200

# 生成缩略图
def generate_thumbnail(input_path, output_path, size=(200, 200)):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path)

@bp.route('/<int:portfolio_id>', methods=['GET'])
def get_images(portfolio_id):
    images = Image.query.filter_by(portfolio_id=portfolio_id).order_by(Image.sort_order).all()
    
    server_url = get_server_url()
    
    return jsonify({
        'images': [{
            'id': img.id,
            'filename': img.filename,
            'filepath': f'{server_url}/uploads/{os.path.basename(img.filepath)}',
            'thumbnail_path': f'{server_url}/uploads/{os.path.basename(img.thumbnail_path)}',
            'sort_order': img.sort_order
        } for img in images]
    }), 200

# 更新图片排序
@bp.route('/sort', methods=['PUT'])
def update_image_order():
    data = request.get_json()
    image_ids = data.get('image_ids', [])
    
    for index, image_id in enumerate(image_ids):
        image = Image.query.get(image_id)
        if image:
            image.sort_order = index + 1
    
    db.session.commit()
    
    return jsonify({'message': 'Image order updated successfully'}), 200

# 删除图片
@bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    # 删除文件
    if os.path.exists(image.filepath):
        os.remove(image.filepath)
    if image.thumbnail_path and os.path.exists(image.thumbnail_path):
        os.remove(image.thumbnail_path)
    
    # 从数据库删除
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': 'Image deleted successfully'}), 200

# 图片滤镜处理
@bp.route('/filter', methods=['POST'])
def apply_filter():
    data = request.get_json()
    image_id = data.get('image_id')
    filter_params = data.get('params', {})
    
    if not image_id:
        return jsonify({'error': 'Image ID is required'}), 400
    
    # 获取图片
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    # 处理图片滤镜
    try:
        result_path = apply_image_filter(image.filepath, filter_params)
        return jsonify({'filtered_image': result_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 应用图片滤镜
def apply_image_filter(image_path, params):
    with Image.open(image_path) as img:
        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 应用亮度调整
        if 'brightness' in params:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1 + params['brightness'] / 100)
        
        # 应用对比度调整
        if 'contrast' in params:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(params['contrast'] / 100)
        
        # 应用饱和度调整
        if 'saturation' in params:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(params['saturation'] / 100)
        
        # 应用锐化调整
        if 'sharpness' in params:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1 + params['sharpness'] / 100)
        
        # 应用模糊
        if 'blur' in params and params['blur'] > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=params['blur']))
        
        # 保存处理后的图片
        output_filename = f"filtered_{uuid.uuid4().hex}.png"
        output_path = os.path.join('temp', output_filename)
        img.save(output_path)
        
        return output_path

# 下载图片
@bp.route('/download/<string:filename>', methods=['GET'])
def download_image(filename):
    return send_from_directory('uploads', filename)