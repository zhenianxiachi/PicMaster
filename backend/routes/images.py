from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageFilter, ImageEnhance
import json
import uuid
from models import db, Image, Portfolio
import rawpy
import io

bp = Blueprint('images', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'raf', 'cr2', 'nef', 'arw', 'dng', 'raw'}
RAW_EXTENSIONS = {'raf', 'cr2', 'nef', 'arw', 'dng', 'raw'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_raw_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in RAW_EXTENSIONS

def get_server_url():
    host = current_app.config.get('SERVER_HOST', 'localhost')
    port = current_app.config.get('SERVER_PORT', '5000')
    return f"http://{host}:{port}"

def convert_raw_to_image(raw_path, output_path):
    with rawpy.imread(raw_path) as raw:
        rgb = raw.postprocess(
            use_camera_wb=True,
            half_size=False,
            no_auto_bright=False,
            output_bps=8
        )
    img = Image.fromarray(rgb)
    img.save(output_path, 'JPEG', quality=95)
    return output_path

@bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('file')
    portfolio_id = request.form.get('portfolio_id')
    
    if not portfolio_id:
        return jsonify({'error': 'Portfolio ID is required'}), 400
    
    portfolio = Portfolio.query.get(portfolio_id)
    if not portfolio:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)
            
            final_path = upload_path
            final_filename = unique_filename
            
            if is_raw_file(filename):
                try:
                    converted_filename = f"{uuid.uuid4().hex}_{os.path.splitext(filename)[0]}.jpg"
                    converted_path = os.path.join(current_app.config['UPLOAD_FOLDER'], converted_filename)
                    convert_raw_to_image(upload_path, converted_path)
                    
                    if os.path.exists(upload_path):
                        os.remove(upload_path)
                    
                    final_path = converted_path
                    final_filename = converted_filename
                    filename = converted_filename
                except Exception as e:
                    print(f"RAW转换失败: {str(e)}")
                    if os.path.exists(upload_path):
                        os.remove(upload_path)
                    continue
            
            thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"thumb_{final_filename}")
            try:
                generate_thumbnail(final_path, thumbnail_path)
            except Exception as e:
                print(f"生成缩略图失败: {str(e)}")
                thumbnail_path = final_path
            
            max_sort = db.session.query(db.func.max(Image.sort_order)).filter_by(portfolio_id=portfolio_id).scalar() or 0
            
            new_image = Image(
                filename=filename,
                filepath=final_path,
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

@bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    if os.path.exists(image.filepath):
        os.remove(image.filepath)
    if image.thumbnail_path and os.path.exists(image.thumbnail_path):
        os.remove(image.thumbnail_path)
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': 'Image deleted successfully'}), 200

@bp.route('/filter', methods=['POST'])
def apply_filter():
    data = request.get_json()
    image_id = data.get('image_id')
    filter_params = data.get('params', {})
    
    if not image_id:
        return jsonify({'error': 'Image ID is required'}), 400
    
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    try:
        result_path = apply_image_filter(image.filepath, filter_params)
        return jsonify({'filtered_image': result_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def apply_image_filter(image_path, params):
    with Image.open(image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        if 'brightness' in params:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1 + params['brightness'] / 100)
        
        if 'contrast' in params:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(params['contrast'] / 100)
        
        if 'saturation' in params:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(params['saturation'] / 100)
        
        if 'sharpness' in params:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1 + params['sharpness'] / 100)
        
        if 'blur' in params and params['blur'] > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=params['blur']))
        
        output_filename = f"filtered_{uuid.uuid4().hex}.png"
        output_path = os.path.join('temp', output_filename)
        img.save(output_path)
        
        return output_path

@bp.route('/download/<string:filename>', methods=['GET'])
def download_image(filename):
    return send_from_directory('uploads', filename)
