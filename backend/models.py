from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库实例
db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

# 作品集分类表
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    portfolios = db.relationship('Portfolio', backref='category', lazy=True)

# 标签表
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 作品集标签关联表
portfolio_tags = db.Table('portfolio_tags',
    db.Column('portfolio_id', db.Integer, db.ForeignKey('portfolios.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

# 作品集表
class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    shoot_date = db.Column(db.Date, nullable=False)
    cover_image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    images = db.relationship('Image', backref='portfolio', lazy=True, order_by='Image.sort_order')
    tags = db.relationship('Tag', secondary=portfolio_tags, lazy='subquery',
                          backref=db.backref('portfolios', lazy=True))

# 图片表
class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    annotations = db.relationship('Annotation', backref='image', lazy=True)

# 滤镜预设表
class FilterPreset(db.Model):
    __tablename__ = 'filter_presets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    params = db.Column(db.JSON, nullable=False)  # 存储滤镜参数JSON
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 客户反馈表
class ClientFeedback(db.Model):
    __tablename__ = 'client_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    feedback_content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 标注表
class Annotation(db.Model):
    __tablename__ = 'annotations'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    annotation_data = db.Column(db.Text, nullable=False)  # 存储标注数据
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 预览链接表
class PreviewLink(db.Model):
    __tablename__ = 'preview_links'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expire_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_valid = db.Column(db.Boolean, default=True)