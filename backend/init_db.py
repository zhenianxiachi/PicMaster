from models import db, User, Category, Tag, FilterPreset
from app import app
from werkzeug.security import generate_password_hash
from datetime import datetime

# 初始化数据库
def init_db():
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 初始化管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin'),
                email='1427844359@qq.com'
            )
            db.session.add(admin)
        else:
            # 更新现有管理员用户信息
            admin.password = generate_password_hash('admin')
            admin.email = '1427844359@qq.com'
            db.session.add(admin)
        
        # 初始化分类
        categories = ['婚礼', '人像', '商业', '风景', '产品', '活动']
        for category_name in categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
        
        # 初始化标签
        tags = ['高清', '精选', '原图', '修图', '调色', '构图', '光影', '创意']
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
        
        # 初始化滤镜预设
        filter_presets = [
            {
                'name': '原图',
                'params': {
                    'brightness': 0,
                    'contrast': 100,
                    'saturation': 100,
                    'hue': 0,
                    'blur': 0,
                    'sharpness': 0,
                    'gamma': 1,
                    'exposure': 0,
                    'shadow': 0,
                    'highlight': 0,
                    'warmth': 50,
                    'vibrance': 100
                },
                'is_public': True
            },
            {
                'name': '清新',
                'params': {
                    'brightness': 20,
                    'contrast': 110,
                    'saturation': 120,
                    'hue': 10,
                    'blur': 0,
                    'sharpness': 20,
                    'gamma': 1.2,
                    'exposure': 10,
                    'shadow': -10,
                    'highlight': 10,
                    'warmth': 40,
                    'vibrance': 130
                },
                'is_public': True
            },
            {
                'name': '复古',
                'params': {
                    'brightness': -10,
                    'contrast': 120,
                    'saturation': 80,
                    'hue': 30,
                    'blur': 0.5,
                    'sharpness': 10,
                    'gamma': 0.8,
                    'exposure': -5,
                    'shadow': 20,
                    'highlight': -10,
                    'warmth': 70,
                    'vibrance': 70
                },
                'is_public': True
            },
            {
                'name': '胶片',
                'params': {
                    'brightness': 5,
                    'contrast': 130,
                    'saturation': 110,
                    'hue': 5,
                    'blur': 0,
                    'sharpness': 30,
                    'gamma': 0.9,
                    'exposure': 5,
                    'shadow': 15,
                    'highlight': 5,
                    'warmth': 60,
                    'vibrance': 120
                },
                'is_public': True
            },
            {
                'name': '黑白',
                'params': {
                    'brightness': 10,
                    'contrast': 120,
                    'saturation': 0,
                    'hue': 0,
                    'blur': 0,
                    'sharpness': 20,
                    'gamma': 1,
                    'exposure': 0,
                    'shadow': 10,
                    'highlight': 10,
                    'warmth': 50,
                    'vibrance': 0
                },
                'is_public': True
            }
        ]
        
        for preset_data in filter_presets:
            preset = FilterPreset.query.filter_by(name=preset_data['name']).first()
            if not preset:
                preset = FilterPreset(
                    name=preset_data['name'],
                    params=preset_data['params'],
                    is_public=preset_data['is_public']
                )
                db.session.add(preset)
        
        # 提交所有更改
        db.session.commit()
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()